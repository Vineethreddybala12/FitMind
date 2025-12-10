
from django.contrib import admin
from django.urls import path
from maini.views import *

urlpatterns = [
    path('', first, name='first'),
    path('dashboard/', dashboard, name='dashboard'),
    path('workouts/', workouts, name='workouts'),
    path('meditation/', meditation, name='meditation'),
    path('nutrition/', nutrition, name='nutrition'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('chatbot/', chatbot, name='chatbot'),
    path('admin/', admin.site.urls),
]
