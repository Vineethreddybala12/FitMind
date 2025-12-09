from django.shortcuts import render

def first(request):
    return render(request, 'first.html')

def login(request):
    return render(request, 'login.html')   # ✅ show login page

def register(request):
    return render(request, 'register.html')

def chatbot(request):
    return render(request, 'chatbot.html')
