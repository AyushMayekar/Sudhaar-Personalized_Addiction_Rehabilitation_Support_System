from django.db import models
from django.contrib.auth.models import User

class Clients(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def _str_(self):
        return self.name 