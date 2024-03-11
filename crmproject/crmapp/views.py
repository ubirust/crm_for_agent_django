from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EmployeeRegistrationForm
from .models import Manager


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
