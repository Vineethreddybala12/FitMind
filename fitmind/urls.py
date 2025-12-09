
from django.contrib import admin
from django.urls import path
from maini.views import *

urlpatterns = [
   path('', first, name='first'),
path('login/', login, name='login'),
path('register/', register, name='register'),
path('chatbot/', chatbot, name='chatbot'),

]
