import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EmployeeRegistrationForm
from .models import Manager, Listing, Employee


class ManagerLoginView(LoginView):
    template_name = 'manager_login.html'


@login_required
def register_employee(request):
    # Проверяем, является ли текущий пользователь менеджером
    try:
        request.user.manager
    except Manager.DoesNotExist:
        return redirect('some_error_page')  # Перенаправляем на страницу ошибки

    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            # Связываем сотрудника с менеджером текущего пользователя
            employee.manager = request.user.manager
            employee.save()
            return redirect('some_success_page')  # Перенаправляем на страницу успеха
    else:
        form = EmployeeRegistrationForm()

    return render(request, 'register_employee.html', {'form': form})


def listings_admin(request):
    listings = Listing.objects.all().order_by('-id')  # Получаем все записи из БД, упорядоченные по ID
    return render(request, 'listing.html', {'listings': listings})  # тестовая версия


def get_employee(request):
    employees = Employee.objects.all().order_by('id')  # Получаем все записи из БД, упорядоченные по ID
    return render(request, 'employee.html', {'employees': employees})


def update_employees(request):
    if request.method == 'POST':
        data = json.loads(request.POST.get('data'))

        for item in data:
            user_id = item['user_id']
            first_name = item['first_name']
            username = item['username']
            plain_password = item['plain_password']

            try:
                user = User.objects.get(id=user_id)
                employee = Employee.objects.get(user=user)
                user.first_name = first_name
                user.username = username
                user.password = make_password(plain_password) # для авторизации сохраняю легкий пароль в базовой модели User
                employee.plain_password = plain_password # это видимый пароль сотрудника, который может быть быстро изменен
                user.save()
                employee.save()
            except User.DoesNotExist:
                pass

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Неверный метод запроса'})


def add_employee(request):
    if request.method == 'POST':
        data = json.loads(request.POST.get('data'))
        print(data)
        for item in data:
            first_name = item['first_name']
            username = item['username']
            plain_password = item['plain_password']

            try:
                # Получаем текущего залогиненного менеджера
                manager = request.user.manager

                # Создаем пользователя
                user = User.objects.create_user(username=username, password=plain_password, first_name=first_name)

                # Создаем сотрудника и связываем его с пользователем и менеджером
                employee = Employee.objects.create(user=user, manager=manager, plain_password=plain_password)
            except Manager.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Менеджер не найден'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})

        return JsonResponse({'success': True})

    return JsonResponse({'status': 'error', 'message': 'Неверный метод запроса'})
