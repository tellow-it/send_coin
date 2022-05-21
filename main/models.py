from django.db import models

from django.db import models


# Create your models here.


class Transaction(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    date_send = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
