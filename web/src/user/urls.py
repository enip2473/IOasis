from django.urls import path
from user.views import UserEditPage

app_name = 'user'

urlpatterns = [
    path('<user_id>/edit/', UserEditPage, name='edit'),
]