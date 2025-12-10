from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from .models import Workout, MealPlan, Meditation, ChatMessage


def first(request):
    return render(request, 'first.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def workouts(request):
    workout_list = Workout.objects.all()
    return render(request, 'workouts.html', {'workouts': workout_list})


def meditation(request):
    meditation_list = Meditation.objects.all()
    return render(request, 'meditation.html', {'meditations': meditation_list})


def nutrition(request):
    meal_list = MealPlan.objects.all()
    return render(request, 'nutrition.html', {'meals': meal_list})


def login(request):
    # Handle POST to authenticate user (we use email as username)
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return render(request, 'login.html')

    return render(request, 'login.html')


def register(request):
    # Handle user registration and auto-login
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'A user with this email already exists. Please login.')
            return redirect('login')

        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        user.save()
        # Auto-login after registration
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Account created and logged in as {user.first_name or user.username}.')
            return redirect('dashboard')
        else:
            messages.success(request, 'Account created. Please login.')
            return redirect('login')

    return render(request, 'register.html')


def logout(request):
    auth_logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('first')


@require_http_methods(["GET", "POST"])
def chatbot(request):
    if request.method == 'GET':
        return render(request, 'chatbot.html')
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            
            if not user_message:
                return JsonResponse({'response': 'Please ask me something!'}, status=400)
            
            # Generate response based on keywords
            response_text = generate_chatbot_response(user_message)
            
            # Save chat message if user is authenticated
            if request.user.is_authenticated:
                ChatMessage.objects.create(
                    user=request.user,
                    message=user_message,
                    response=response_text
                )
            
            return JsonResponse({'response': response_text})
        
        except json.JSONDecodeError:
            return JsonResponse({'response': 'Invalid request format.'}, status=400)
        except Exception as e:
            return JsonResponse({'response': 'An error occurred. Please try again.'}, status=500)


def generate_chatbot_response(user_message):
    """Generate AI-like responses based on fitness and wellness keywords"""
    message_lower = user_message.lower()
    
    # Fitness & Workout responses
    if any(word in message_lower for word in ['workout', 'exercise', 'training', 'gym', 'fit']):
        responses = [
            "Great! Regular workouts are essential for fitness. Mix cardio, strength training, and flexibility exercises. Aim for at least 150 minutes of moderate activity per week.",
            "Exercise is fantastic! Start with 20-30 minute sessions, 3-4 times a week. Include warm-ups and cool-downs. What type of workout interests you?",
            "Consistency is key to fitness! Try different workouts to stay motivated: running, cycling, strength training, or our FitMind workouts.",
        ]
        return responses[hash(user_message) % len(responses)]
    
    # Nutrition & Diet responses
    if any(word in message_lower for word in ['diet', 'food', 'nutrition', 'eat', 'meal', 'calories', 'protein']):
        responses = [
            "Nutrition is crucial! Eat balanced meals with proteins, carbs, and healthy fats. Drink plenty of water and avoid processed foods.",
            "Good nutrition fuels your workouts! Focus on whole foods, vegetables, lean proteins, and whole grains. Check our meal plans for ideas.",
            "Remember: nutrition isn't about restriction—it's about nourishing your body. Eat mindfully and enjoy your food!",
        ]
        return responses[hash(user_message) % len(responses)]
    
    # Meditation & Mental Health responses
    if any(word in message_lower for word in ['meditation', 'stress', 'anxiety', 'mindfulness', 'relax', 'peace', 'calm']):
        responses = [
            "Meditation is powerful for mental health! Start with just 5-10 minutes daily. Focus on your breathing and let thoughts pass without judgment.",
            "Stress relief is important. Try our meditation sessions, deep breathing exercises, or yoga. Even 10 minutes of mindfulness helps!",
            "Mental wellness is as important as physical fitness. Regular meditation reduces anxiety and improves focus. Try our guided sessions!",
        ]
        return responses[hash(user_message) % len(responses)]
    
    # Weight loss responses
    if any(word in message_lower for word in ['weight', 'lose', 'fat', 'slim', 'body weight']):
        responses = [
            "Weight loss takes time and consistency. Combine a balanced diet with regular exercise. Focus on losing 1-2 pounds per week safely.",
            "For healthy weight loss: create a small calorie deficit, eat protein-rich foods, stay hydrated, and exercise regularly.",
            "Remember, weight is just a number. Focus on building muscle, eating well, and exercising. Progress comes in many forms!",
        ]
        return responses[hash(user_message) % len(responses)]
    
    # General wellness
    if any(word in message_lower for word in ['water', 'sleep', 'rest', 'hydrate', 'health']):
        responses = [
            "Stay hydrated! Drink at least 8 glasses of water daily. Sleep 7-9 hours per night for recovery and wellness.",
            "Wellness includes rest and recovery. Don't skip sleep—it's when your body repairs and builds muscle.",
            "Balance is key: exercise, nutrition, sleep, and stress management. All work together for optimal health!",
        ]
        return responses[hash(user_message) % len(responses)]
    
    # Motivation & General encouragement
    if any(word in message_lower for word in ['help', 'motivation', 'stuck', 'advice', 'tip']):
        responses = [
            "I'm here to help! Tell me more about your fitness goals and I can provide personalized guidance.",
            "You've got this! Starting is the hardest part. Set small goals, stay consistent, and celebrate progress!",
            "Every journey starts with a single step. Whether it's fitness, nutrition, or wellness—I'm here to support you!",
        ]
        return responses[hash(user_message) % len(responses)]
    
    # Default friendly response
    default_responses = [
        "That's a great question! I'm designed to help with fitness, nutrition, meditation, and wellness. Ask me anything in these areas!",
        "I'm here to help with your fitness journey. Feel free to ask about workouts, nutrition, meditation, or wellness tips!",
        "I'm your FitMind Assistant! Ask me about exercises, meal plans, meditation, or any health and wellness topic.",
        "Great question! I'm equipped to help with fitness, nutrition, mental wellness, and overall health. What would you like to know?",
    ]
    return default_responses[hash(user_message) % len(default_responses)]
