from django.db import models
from django.contrib.auth.models import User


class Events(models.Model):
    """
    Таблица: События
    """
    date_start = models.BigIntegerField(null=False, default=0)
    name = models.CharField(blank=False, max_length=40)
    period = models.IntegerField(blank=True, null=False, default=0)
    archive = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None, blank=True, null=True)