from django.contrib.auth.models import User
from django.db import models


class Agency(models.Model):
    name = models.CharField(max_length=255)


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)


class Listing(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    link = models.URLField(max_length=500)
    phone_number = models.CharField(max_length=20)
    responsible = models.ForeignKey(Employee, on_delete=models.CASCADE)
    call_status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
