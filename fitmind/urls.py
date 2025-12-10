
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
    # API for chat sessions
    path('api/chatsessions/', api_chatsessions, name='api_chatsessions'),
    path('api/chatsessions/<int:session_id>/messages/', api_session_messages, name='api_session_messages'),
    path('api/profile/', api_profile, name='api_profile'),
    path('admin/', admin.site.urls),
]
