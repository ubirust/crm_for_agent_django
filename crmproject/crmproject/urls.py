"""
URL configuration for crmproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from crmapp.views import register_employee, ManagerLoginView, EmployeeLoginView, listings_admin, get_employee, update_employees, add_employee, delete_employee, listings_employee, ListingApiView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/employee/', register_employee, name='register_employee'),
    path('manager/login/', ManagerLoginView.as_view(), name='manager_login'),
    path('login/', EmployeeLoginView.as_view(), name='employee_login'),
    path('manager/listings/', listings_admin, name='listings'),
    path('manager/employs/', get_employee, name='get_employee'),
    path('update_employees/', update_employees, name='update_employees'),
    path('add_employee/', add_employee, name='add_employee'),
    path('delete_employee/', delete_employee, name='delete_employee'),
    path('listings/', listings_employee, name='listings_employee'),
    path('api/v1/listinglist/', ListingApiView.as_view()),
]
