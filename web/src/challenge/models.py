from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Challenge(models.Model):
    guild = models.CharField(max_length=17, validators=[RegexValidator(regex='^$|^[0-9]{17}$', message='Length has to be 17', code='nomatch')], null=True, blank=True)
    username = models.CharField(max_length=25)
    CF_handle = models.CharField(max_length=24, validators=[RegexValidator(regex='^$|^.{3,24}$', message='Length has to be in 3~24', code='nomatch')], null=True, blank=True, unique=True)
    ProblemName = models.CharField(max_length=100)
    Difficulty = models.IntegerField(default=0)
    Time = models.DateTimeField()