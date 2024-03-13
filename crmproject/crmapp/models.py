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
    plain_password = models.CharField(max_length=255, blank=True) # не зашифрованный пароль для быстрого изменения/напоминания


class Listing(models.Model):
    # для быстрого обращения, по типу if listing.call_status == Listing.NEW:
    NEW = 'Новое'
    MISSED = 'Не снял'
    NOT_REACHED = 'Не дозвонился'
    OUR_OBJECT = 'Наш объект'

    CALL_STATUS_CHOICES = [
        (NEW, 'Новое'),
        (MISSED, 'Не снял'),
        (NOT_REACHED, 'Не дозвонился'),
        (OUR_OBJECT, 'Наш объект'),
    ]

    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    link = models.URLField(max_length=500)
    phone_number = models.CharField(max_length=20)
    responsible = models.ForeignKey(Employee, on_delete=models.CASCADE)
    call_status = models.CharField(max_length=100, choices=CALL_STATUS_CHOICES, default=NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)


class OurListings(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True)
