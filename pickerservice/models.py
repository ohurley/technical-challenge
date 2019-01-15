from django.db import models
from simple_history.models import HistoricalRecords


class Solver(models.Model):
    problem = models.CharField(max_length=200)
    username = models.CharField(max_length=200, default='alyien')
    req_date = models.DateTimeField('request published')
    history = HistoricalRecords()


