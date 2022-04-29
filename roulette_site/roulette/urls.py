from django.urls import path
from .views import *

urlpatterns = [
    path('', ShowMainPage.as_view(), name='roulette_main_page'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', show_user_profile, name='profile'),
]