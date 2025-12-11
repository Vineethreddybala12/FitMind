from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import os
import requests
import json
from .models import Workout, MealPlan, Meditation, ChatMessage
from .models import Workout, MealPlan, Meditation, ChatMessage, ChatSession, SessionMessage, UserProfile


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


@csrf_exempt
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
            
            print(f"[DEBUG] Received message: {user_message}")
            print(f"[DEBUG] User authenticated: {request.user.is_authenticated}")
            print(f"[DEBUG] User: {request.user.username if request.user.is_authenticated else 'Anonymous'}")
            
            # Get user profile if authenticated
            profile = None
            if request.user.is_authenticated:
                try:
                    profile = UserProfile.objects.get(user=request.user)
                    print(f"[DEBUG] Profile loaded: age={profile.age}, BMI={profile.bmi()}, stress={profile.stress_level}, activity_level={profile.activity_level}")
                except UserProfile.DoesNotExist:
                    profile = None
                    print("[DEBUG] No profile found for user")
            else:
                print("[DEBUG] User not authenticated")
            
            # Generate response based on profile and message
            response_text = generate_chatbot_response(user_message, profile)
            print(f"[DEBUG] Generated response: {response_text[:100]}...")
            
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
            print(f"[DEBUG] Exception: {str(e)}")
            import traceback
            traceback.print_exc()
            return JsonResponse({'response': 'An error occurred. Please try again.'}, status=500)


def generate_chatbot_response(user_message, profile=None):
    """Generate personalized responses based on message and user profile."""
    message_lower = user_message.lower()
    words = set(message_lower.split())

    # Safety checks for crisis language
    crisis_terms = ['suicide', 'self-harm', 'kill myself', "i can't go on", 'hurt myself', 'want to die']
    if any(term in message_lower for term in crisis_terms):
        direct = "I’m really sorry you’re feeling this way — I’m here with you."
        guidance = (
            "If you are in immediate danger, please call your local emergency services right now. "
            "If you can, reach out to a trusted person and tell them how you’re feeling. "
            "Consider contacting a mental health professional or crisis line in your area."
        )
        motivation = "You don’t have to go through this alone — please seek help right away."
        return f"Direct Answer: {direct}\n\nPersonalized Guidance: {guidance}\n\nMotivation Line: {motivation}"

    # Meditation & Mindfulness
    meditation_keywords = {'meditation', 'mindfulness', 'breathe', 'breathing', 'relax', 'relaxation', 'calm', 'peace', 'focus', 'anxiety', 'worry'}
    if any(word in words for word in meditation_keywords) or 'stress' in message_lower:
        direct = "Try a short guided breathing practice to settle your mind."
        if profile and profile.stress_level == 'high':
            direct += " Given your high stress level, this is especially important for you."
        
        guidance = ("1) Sit comfortably and close your eyes. 2) Inhale for 4 counts, hold 1, exhale for 6 — repeat 6 times. "
                    "3) If you have 5 minutes, try a body-scan: notice toes → legs → torso → shoulders → jaw.")
        
        if profile and profile.sleep_hours and profile.sleep_hours < 6:
            guidance += f"\n\nNote: Your sleep is low ({profile.sleep_hours}hrs). Meditation can help improve sleep quality."
        
        motivation = "Small practices add up — great choice taking this step."
        return f"Direct Answer: {direct}\n\nPersonalized Guidance: {guidance}\n\nMotivation Line: {motivation}"

    # Workout & Exercise
    workout_keywords = {'workout', 'exercise', 'training', 'gym', 'pushups', 'squat', 'fitness', 'run', 'walk', 'cardio', 'strength', 'sport', 'active', 'move'}
    if any(word in words for word in workout_keywords):
        direct = "You can do a short, effective bodyweight workout right now."
        
        # Personalize based on activity level
        if profile:
            if profile.activity_level == 'low':
                direct += " Since you have low activity, start with gentle movements and build up gradually."
                guidance = ("1) Warm-up 2 minutes (slow marching, arm circles). 2) Circuit — 2 rounds: 5 squats, 5 push-ups (knees ok), 10s plank. "
                           "3) Cool down with stretching. Total time ~10 minutes.")
            elif profile.activity_level == 'high':
                direct += " Since you're already active, let's intensify it!"
                guidance = ("1) Warm-up 5 minutes. 2) Circuit — 4 rounds: 15 squats, 15 push-ups, 30s plank, 20 jumping jacks. "
                           "3) Cool down. Total time ~25 minutes.")
            else:
                guidance = ("1) Warm-up 3 minutes (march in place, arm circles). 2) Circuit — 3 rounds: 10 squats, 10 push-ups (knees ok), 20s plank. "
                           "3) Cool down with light stretching. Total time ~15–20 minutes.")
        else:
            guidance = ("1) Warm-up 3 minutes. 2) Circuit — 3 rounds: 10 squats, 10 push-ups, 20s plank. "
                       "3) Cool down with stretching. Total time ~15–20 minutes.")
        
        if profile and profile.sleep_hours and profile.sleep_hours < 6:
            guidance += f"\n\nTip: Your sleep is low ({profile.sleep_hours}hrs). Good recovery sleep helps. Prioritize sleep tonight!"
        
        motivation = "Consistency beats intensity — you're building a healthy habit."
        return f"Direct Answer: {direct}\n\nPersonalized Guidance: {guidance}\n\nMotivation Line: {motivation}"

    # Nutrition & Diet
    nutrition_keywords = {'diet', 'nutrition', 'meal', 'calories', 'protein', 'vegetarian', 'vegan', 'snack', 'eat', 'food', 'weight', 'cook', 'recipe', 'healthy'}
    if any(word in words for word in nutrition_keywords):
        direct = "Aim for balanced meals with protein, vegetables, and whole grains."
        
        # Personalize based on BMI
        if profile:
            bmi = profile.bmi()
            if bmi and bmi > 25:
                direct += f" Your BMI is {bmi:.1f} ({profile.bmi_category()}). Focus on whole foods and portion control."
            elif bmi and bmi < 18.5:
                direct += f" Your BMI is {bmi:.1f} ({profile.bmi_category()}). Eat enough calories with nutrient-dense foods."
        
        guidance = ("1) Swap refined carbs for whole grains (brown rice, whole wheat bread). "
                   "2) Add a protein source each meal (eggs, lentils, tofu, chicken). "
                   "3) For late-night cravings try a small protein-rich snack: Greek yogurt or a handful of nuts.")
        
        if profile and profile.stress_level == 'high':
            guidance += "\n\nTip: Reduce caffeine and sugar during stressful times — they can increase anxiety."
        
        motivation = "Small swaps make big differences over time — you've got this."
        return f"Direct Answer: {direct}\n\nPersonalized Guidance: {guidance}\n\nMotivation Line: {motivation}"

    # Sleep & Rest
    sleep_keywords = {'sleep', 'insomnia', 'tired', 'rest', 'fatigue', 'sleepy', 'awake', 'bed', 'nap', 'dream'}
    if any(word in words for word in sleep_keywords):
        direct = "Improve sleep with a consistent wind-down routine."
        
        if profile and profile.sleep_hours:
            if profile.sleep_hours < 6:
                direct += f" You're sleeping {profile.sleep_hours} hours — aiming for 7-9 is ideal."
            elif profile.sleep_hours > 9:
                direct += f" You're sleeping {profile.sleep_hours} hours — if you're still tired, check sleep quality, not just quantity."
        
        guidance = ("1) Regular sleep schedule: same bedtime/wake time every day. 2) Reduce screens 30–60 mins before bed. "
                   "3) Try a 10-minute relaxation: diaphragmatic breathing or progressive muscle relaxation.")
        
        if profile and profile.activity_level == 'low':
            guidance += "\n\nTip: Light exercise during the day helps sleep — even a 20-minute walk improves rest."
        
        motivation = "Better sleep improves everything — small changes help a lot."
        return f"Direct Answer: {direct}\n\nPersonalized Guidance: {guidance}\n\nMotivation Line: {motivation}"

    # Mental Health & Mood (new)
    mood_keywords = {'mood', 'happy', 'sad', 'depressed', 'energy', 'motivation', 'confidence', 'brain', 'mental', 'feeling', 'emotion'}
    if any(word in words for word in mood_keywords):
        direct = "Taking care of your mental health is just as important as physical fitness."
        
        if profile:
            suggestions = []
            if profile.stress_level == 'high':
                suggestions.append("meditation or breathing exercises (you have high stress)")
            if profile.sleep_hours and profile.sleep_hours < 6:
                suggestions.append("improving sleep (you're sleeping less than ideal)")
            if profile.activity_level == 'low':
                suggestions.append("light exercise (movement boosts mood)")
            
            if suggestions:
                direct += f" Try: {', '.join(suggestions)}."
        
        guidance = ("1) Start your day with 5 minutes of gratitude or journaling. "
                   "2) Move your body — even a 10-minute walk releases feel-good chemicals. "
                   "3) Connect with someone or practice self-compassion.")
        
        motivation = "Small daily wins compound — you're investing in yourself."
        return f"Direct Answer: {direct}\n\nPersonalized Guidance: {guidance}\n\nMotivation Line: {motivation}"

    # Habit Building (new)
    habit_keywords = {'habit', 'routine', 'goal', 'progress', 'improve', 'change', 'build', 'track', 'consistency'}
    if any(word in words for word in habit_keywords):
        direct = "Building healthy habits takes patience and self-compassion."
        
        guidance = ("1) Start small: one tiny habit (5 min). 2) Track daily for a week — see momentum. "
                   "3) Add the next habit when the first feels automatic (usually ~2–3 weeks).")
        
        if profile:
            guidance += f"\n\nYour profile shows stress level '{profile.stress_level}' and activity '{profile.activity_level}' — start with what feels manageable!"
        
        motivation = "Progress over perfection — every small step counts."
        return f"Direct Answer: {direct}\n\nPersonalized Guidance: {guidance}\n\nMotivation Line: {motivation}"

    # General wellness question or short message
    if len(user_message.split()) < 6 or user_message.endswith('?'):
        direct = "I can help with meditation, workouts, nutrition, sleep, mood, and habit-building."
        
        if profile:
            # Suggest based on profile weaknesses
            suggestions = []
            if profile.stress_level == 'high':
                suggestions.append("meditation (your stress is high)")
            if profile.sleep_hours and profile.sleep_hours < 6:
                suggestions.append("sleep routine (your sleep is low)")
            if profile.activity_minutes and profile.activity_minutes < 30:
                suggestions.append("a quick workout (boost your activity)")
            if not profile.age:
                suggestions.append("set up your profile (helps me personalize better)")
            
            if suggestions:
                direct += f"\n\nTry: {', '.join(suggestions)}."
        
        motivation = "Tell me more and I'll give you a short, practical plan!"
        return f"Direct Answer: {direct}\n\nMotivation Line: {motivation}"

    # Default friendly, helpful reply
    direct = "I can help with meditation, workouts, nutrition, sleep, mood, and habit-building. What would you like help with?"
    guidance = "Choose one topic: meditation (5 min), a quick workout (15 min), a meal swap, better sleep, or building a habit. I'll give a short plan."
    
    if profile:
        bmi = profile.bmi()
        guidance += f"\n\nYour profile shows: BMI {bmi:.1f} ({profile.bmi_category()}), stress level '{profile.stress_level}', activity level '{profile.activity_level}'. I can tailor advice!"
    
    motivation = "You're taking a great step — let's make it simple and do-able."
    return f"Direct Answer: {direct}\n\nPersonalized Guidance: {guidance}\n\nMotivation Line: {motivation}"


# --- New API endpoints for chat sessions and Gemini relay ---
@require_http_methods(["GET", "POST"])
def api_chatsessions(request):
    # List or create chat sessions for the authenticated user
    if not request.user.is_authenticated:
        return HttpResponseForbidden('Authentication required')

    if request.method == 'GET':
        sessions = request.user.chat_sessions.all().order_by('-updated_at')
        data = [{'id': s.id, 'title': s.title, 'updated_at': s.updated_at.isoformat()} for s in sessions]
        return JsonResponse({'sessions': data})

    # POST -> create new session with optional title
    try:
        payload = json.loads(request.body or '{}')
    except Exception:
        payload = {}
    title = payload.get('title') or 'New chat'
    sess = ChatSession.objects.create(user=request.user, title=title)
    return JsonResponse({'id': sess.id, 'title': sess.title})


@require_http_methods(["GET", "POST"])
def api_session_messages(request, session_id):
    # Get or append messages for a given session. Posting a user message will relay to Gemini and save assistant reply.
    if not request.user.is_authenticated:
        return HttpResponseForbidden('Authentication required')

    try:
        session = ChatSession.objects.get(id=session_id, user=request.user)
    except ChatSession.DoesNotExist:
        return JsonResponse({'error': 'session not found'}, status=404)

    if request.method == 'GET':
        msgs = [{'role': m.role, 'content': m.content, 'created_at': m.created_at.isoformat()} for m in session.messages.all()]
        return JsonResponse({'messages': msgs, 'session': {'id': session.id, 'title': session.title}})

    # POST: user sends message -> save, send to Gemini, save assistant reply, return reply
    try:
        data = json.loads(request.body)
        user_text = data.get('message', '').strip()
        if not user_text:
            return JsonResponse({'error': 'empty message'}, status=400)

        # Save user message
        SessionMessage.objects.create(session=session, role='user', content=user_text)

        # Build simple context: last N messages
        history = session.messages.all().order_by('created_at')
        prompt_parts = []
        for m in history:
            prompt_parts.append(f"{m.role}: {m.content}")
        prompt_parts.append(f"user: {user_text}")
        prompt = "\n".join(prompt_parts[-20:])

        # Call Gemini
        assistant_reply = call_gemini(prompt)

        # Save assistant reply
        SessionMessage.objects.create(session=session, role='assistant', content=assistant_reply)
        session.updated_at = session.updated_at
        session.save()

        return JsonResponse({'reply': assistant_reply})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'invalid json'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def call_gemini(prompt_text: str) -> str:
    """Relay function to call Google Gemini 2.5 Flash via the Generative API.
    Requires environment variable `GOOGLE_API_KEY` (API key) or `GOOGLE_API_BEARER` (Bearer token).
    Falls back to a helpful message if there's an error.
    """
    api_key = os.environ.get('GOOGLE_API_KEY')
    bearer = os.environ.get('GOOGLE_API_BEARER')

    url = 'https://generativelanguage.googleapis.com/v1beta2/models/gemini-2.5-flash:generateMessage'
    headers = {'Content-Type': 'application/json'}
    params = {}
    if api_key:
        params['key'] = api_key
    elif bearer:
        headers['Authorization'] = f'Bearer {bearer}'
    else:
        return "(Gemini not configured) Please set GOOGLE_API_KEY or GOOGLE_API_BEARER on the server."

    # Prepend a system-style FitMind prompt to guide Gemini's behavior
    system_prompt = (
        "You are FitMind — an intelligent, friendly, and supportive wellness chatbot. "
        "Guide users across meditation, fitness, nutrition, sleep, mood, and habit-building. "
        "Always be positive, ask clarifying questions only when needed, provide short actionable steps, and for any indication of self-harm or emergency encourage contacting local emergency services and a professional. "
        "Return concise outputs in three parts: Direct Answer, Personalized Guidance, Motivation Line."
    )

    body = {
        'messages': [
            { 'author': 'system', 'content': [ { 'type': 'text', 'text': system_prompt } ] },
            { 'author': 'user', 'content': [ { 'type': 'text', 'text': prompt_text } ] }
        ],
        'maxOutputTokens': 512,
    }

    try:
        resp = requests.post(url, headers=headers, params=params, json=body, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        # Try to extract text from the response in a few common locations
        # Typical structure: { 'candidates': [ { 'content': [ { 'type': 'output_text', 'text': '...' } ] } ] }
        text = None
        if isinstance(data, dict):
            # check 'candidates'
            candidates = data.get('candidates') or data.get('responses') or []
            if candidates and isinstance(candidates, list):
                first = candidates[0]
                # search in nested content
                content = first.get('content') or first.get('message') or []
                if isinstance(content, list) and len(content) > 0:
                    # find first item with a text-like key
                    for c in content:
                        if isinstance(c, dict) and ('text' in c):
                            text = c.get('text')
                            break
                # fallback: first.get('text')
                if not text:
                    text = first.get('text')

        if not text:
            # try alternate field
            text = data.get('output', {}).get('content', '') if isinstance(data, dict) else None

        return text or "(No response from Gemini)"

    except Exception as e:
        return f"(Gemini call failed) {str(e)}"


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_profile(request):
    """Get or update the authenticated user's profile."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=403)

    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'GET':
        data = {
            'profile': {
                'age': profile.age,
                'height_cm': profile.height_cm,
                'weight_kg': profile.weight_kg,
                'sleep_hours': profile.sleep_hours,
                'activity_minutes': profile.activity_minutes,
                'activity_level': profile.activity_level,
                'stress_level': profile.stress_level,
                'bmi': profile.bmi(),
                'bmi_category': profile.bmi_category(),
            }
        }
        return JsonResponse(data)

    # POST -> update
    try:
        payload = json.loads(request.body or '{}')
    except Exception as e:
        return JsonResponse({'error': f'Invalid JSON: {str(e)}'}, status=400)

    # Accept numeric fields if present
    for fld in ['age', 'height_cm', 'weight_kg', 'sleep_hours', 'activity_minutes']:
        if fld in payload:
            try:
                val = payload.get(fld)
                if val is not None:
                    setattr(profile, fld, val)
            except Exception as e:
                print(f'Error setting {fld}: {e}')

    for fld in ['activity_level', 'stress_level']:
        if fld in payload and payload.get(fld) is not None:
            setattr(profile, fld, payload.get(fld))

    try:
        profile.save()
    except Exception as e:
        return JsonResponse({'error': f'Save error: {str(e)}'}, status=500)

    return JsonResponse({
        'ok': True,
        'profile': {
            'age': profile.age,
            'height_cm': profile.height_cm,
            'weight_kg': profile.weight_kg,
            'sleep_hours': profile.sleep_hours,
            'activity_minutes': profile.activity_minutes,
            'activity_level': profile.activity_level,
            'stress_level': profile.stress_level,
            'bmi': profile.bmi(),
            'bmi_category': profile.bmi_category(),
        }
    })
