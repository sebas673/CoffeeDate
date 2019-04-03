from django.db import models
from django.contrib.auth.models import User


class Preferences(models.Model):
    pref1 = models.PositiveSmallIntegerField(default=0)
    pref2 = models.PositiveSmallIntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class WeeklyMatch(models.Model):
    matchID = models.PositiveIntegerField(default=0)