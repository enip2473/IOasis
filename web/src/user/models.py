from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy
from django.core.validators import RegexValidator

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(ugettext_lazy('email address'), unique=True)
    # some variables accept null values, custom after register
    # guild is use for Discord app
    guild = models.CharField(max_length=17, validators=[RegexValidator(regex='^$|^[0-9]{17}$', message='Length has to be 17', code='nomatch')], null=True, blank=True)
    username = models.CharField(max_length=25, unique=True)
    #avatar = models.ImageField()
    
    # OJ Config
    CF_handle = models.CharField(max_length=24, validators=[RegexValidator(regex='^$|^.{3,24}$', message='Length has to be in 3~24', code='nomatch')], null=True, blank=True, unique=True)
    
    # Rating Status
    Implementation_rating = models.IntegerField(default=0)
    DP_rating = models.IntegerField(default=0)
    Graph_rating = models.IntegerField(default=0)
    Math_rating = models.IntegerField(default=0)
    DataStructure_rating = models.IntegerField(default=0)
    Greedy_rating = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'UserConfig'