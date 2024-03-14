import json
from datetime import datetime
from time import localtime

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from rest_framework import generics, status
from asgiref.sync import async_to_sync
from .forms import EmployeeRegistrationForm
from .models import Manager, Listing, Employee, OurListings
from .serializers import ListingSerializer


class ManagerLoginView(LoginView):
    template_name = 'manager_login.html'


class EmployeeLoginView(LoginView):
    template_name = 'employee_login.html'


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


def listings_admin(request): # manager/listings/ страница "Все объявления, интерфейс Менеджера"
    listings_count = Listing.objects.count()  # Получаем количество объектов из базы данных
    listings = Listing.objects.all().order_by('-id')  # Получаем все записи из БД, упорядоченные по ID
    return render(request, 'listing_manager.html', {'listings': listings, 'listings_count': listings_count})  # тестовая версия


def get_employee(request): # manager/employs/ страница "Сотрудники"
    employees = Employee.objects.all().order_by('id')  # Получаем все записи из БД, упорядоченные по ID
    return render(request, 'employee.html', {'employees': employees})


def update_employees(request): # update_employees/
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
                # Возвращаем user_id созданного сотрудника в JSON-ответе
                return JsonResponse({'success': True, 'user_id': user.id})
            except Manager.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Менеджер не найден'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Неверный метод запроса'})


def delete_employee(request):
    if request.method == 'POST':
        user_id = request.POST.get('employee_id')

        try:
            user = User.objects.get(id=user_id)
            employee = Employee.objects.get(user=user)
            employee.delete()
            user.delete()
        except User.DoesNotExist:
            pass

        return JsonResponse({'status':'success'})

    return JsonResponse({'status': 'error','message': 'Неверный метод запроса'})


@login_required
def listings_employee(request):
    employee = Employee.objects.get(user=request.user)  # Получаем сотрудника для текущего пользователя
    listings_count = Listing.objects.filter(responsible=employee).count()  # Получаем количество объявлений для этого сотрудника
    our_listings_count = OurListings.objects.filter(
        listing__responsible=employee).count()  # Получаем количество наших квартир для этого сотрудника
    not_agree_status = Listing.objects.filter(responsible=employee, call_status=Listing.MISSED).count()  # Получаем количество статусов звонка "Не договорился" для этого сотрудника
    not_phone_status = Listing.objects.filter(responsible=employee, call_status=Listing.NOT_REACHED).count()  # Получаем количество статусов звонка "Не дозвонился" для этого сотрудника
    #listings = Listing.objects.filter(responsible=employee).order_by('-id')  # Получаем все записи для этого сотрудника, упорядоченные по ID
    listings = Listing.objects.all().order_by('-id')  # Получаем ВСЕ записи из БД, упорядоченные по ID
    return render(request, 'employee/listing.html',
                  {'listings': listings, 'listings_count': listings_count, 'our_listings_count': our_listings_count,
                   'not_agree_status': not_agree_status, 'not_phone_status': not_phone_status, })



# CreateAPIView это обработка Post запросов в rest_framework. perform_create автоматически вызывается в процессе обработки POST-запроса
class ListingApiView(generics.CreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    def perform_create(self, serializer):
        serializer.save()  # Сохранение объекта Listing
        print("Код здесь 3")
        new_listing_data = serializer.data  # Получение данных сохраненного объекта из Баз данных
        # Форматирование даты и времени
        # Преобразование строки в объект datetime
        created_at = datetime.strptime(new_listing_data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        formatted_datetime = created_at.strftime("%d.%m.%Y %H:%M:%S")
        new_listing_data['created_at'] = formatted_datetime
        print(new_listing_data)
        # Далее идет код для отправки данных через WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "listings",  # Название группы, установленное в потребителе
            {
                "type": "listing_message",  # Метод в потребителе, который вызывается
                "listing": new_listing_data  # Данные объявления
            }
        )
