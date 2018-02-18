from django.db import models

class List(models.Model):
    pass

class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, null=True, on_delete=models.SET_NULL)


# Create your models here.
