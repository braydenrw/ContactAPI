from django.db import models
from django.utils import timezone


class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    physical_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.name
