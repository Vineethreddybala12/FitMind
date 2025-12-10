import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitmind.settings')
django.setup()

from maini.models import Workout, MealPlan, Meditation

# Sample Workouts - Physical Prime Section
workouts = [
    {
        'name': 'Morning Run',
        'description': 'A brisk 5km morning run to energize your body and boost metabolism.',
        'intensity': 'medium',
        'duration_minutes': 30,
        'calories_burned': 300,
    },
    {
        'name': 'HIIT Training',
        'description': 'High-Intensity Interval Training combining cardio bursts with strength exercises.',
        'intensity': 'high',
        'duration_minutes': 25,
        'calories_burned': 350,
    },
    {
        'name': 'Yoga Flow',
        'description': 'Relaxing yoga session combining stretching and mindfulness.',
        'intensity': 'low',
        'duration_minutes': 45,
        'calories_burned': 150,
    },
    {
        'name': 'Weight Training',
        'description': 'Strength building workout focusing on major muscle groups.',
        'intensity': 'high',
        'duration_minutes': 50,
        'calories_burned': 400,
    },
    {
        'name': 'Cycling',
        'description': 'Outdoor or indoor cycling for endurance and leg strength.',
        'intensity': 'medium',
        'duration_minutes': 40,
        'calories_burned': 320,
    },
]

# Sample Meal Plans - Nutrition Section
meal_plans = [
    {
        'name': 'Grilled Chicken Salad',
        'meal_type': 'lunch',
        'description': 'Protein-rich grilled chicken with fresh organic vegetables and olive oil dressing.',
        'calories': 450,
        'protein_grams': 45.0,
        'carbs_grams': 25.0,
        'fat_grams': 15.0,
        'ingredients': 'Chicken breast, Lettuce, Tomato, Cucumber, Olive oil, Lemon juice, Salt, Pepper',
        'preparation_time': 20,
    },
    {
        'name': 'Green Smoothie Bowl',
        'meal_type': 'breakfast',
        'description': 'Nutritious smoothie bowl with spinach, berries, and granola.',
        'calories': 350,
        'protein_grams': 15.0,
        'carbs_grams': 55.0,
        'fat_grams': 8.0,
        'ingredients': 'Spinach, Banana, Berries, Greek yogurt, Granola, Honey, Almond milk',
        'preparation_time': 10,
    },
    {
        'name': 'Salmon with Quinoa',
        'meal_type': 'dinner',
        'description': 'Omega-3 rich salmon with healthy quinoa and steamed vegetables.',
        'calories': 550,
        'protein_grams': 50.0,
        'carbs_grams': 45.0,
        'fat_grams': 20.0,
        'ingredients': 'Salmon fillet, Quinoa, Broccoli, Carrot, Olive oil, Garlic, Lemon',
        'preparation_time': 30,
    },
    {
        'name': 'Protein Energy Balls',
        'meal_type': 'snack',
        'description': 'Homemade energy balls packed with protein and natural sweetness.',
        'calories': 120,
        'protein_grams': 10.0,
        'carbs_grams': 15.0,
        'fat_grams': 5.0,
        'ingredients': 'Peanut butter, Oats, Honey, Dark chocolate chips, Chia seeds',
        'preparation_time': 15,
    },
    {
        'name': 'Vegetable Stir Fry',
        'meal_type': 'lunch',
        'description': 'Colorful vegetable stir-fry with tofu and brown rice.',
        'calories': 420,
        'protein_grams': 18.0,
        'carbs_grams': 52.0,
        'fat_grams': 12.0,
        'ingredients': 'Tofu, Broccoli, Bell pepper, Soy sauce, Sesame oil, Ginger, Garlic, Brown rice',
        'preparation_time': 25,
    },
]

# Sample Meditations - Personalized/Stress Relief Section
meditations = [
    {
        'title': 'Morning Mindfulness',
        'description': 'Start your day with a calming 10-minute mindfulness meditation.',
        'difficulty': 'beginner',
        'duration_minutes': 10,
        'instructor': 'Sarah Johnson',
        'meditation_type': 'Mindfulness',
        'benefits': 'Increases focus, reduces anxiety, enhances mental clarity',
    },
    {
        'title': 'Stress Relief Breathing',
        'description': 'Learn breathing techniques to instantly calm your nervous system.',
        'difficulty': 'beginner',
        'duration_minutes': 8,
        'instructor': 'Dr. Michael Chen',
        'meditation_type': 'Breathing',
        'benefits': 'Reduces stress, lowers blood pressure, improves relaxation',
    },
    {
        'title': 'Deep Sleep Visualization',
        'description': 'A guided visualization to help you drift into peaceful, restorative sleep.',
        'difficulty': 'intermediate',
        'duration_minutes': 20,
        'instructor': 'Emma Williams',
        'meditation_type': 'Visualization',
        'benefits': 'Improves sleep quality, reduces insomnia, promotes relaxation',
    },
    {
        'title': 'Body Scan Meditation',
        'description': 'Systematic relaxation technique scanning through your entire body.',
        'difficulty': 'beginner',
        'duration_minutes': 15,
        'instructor': 'David Kumar',
        'meditation_type': 'Mindfulness',
        'benefits': 'Reduces tension, increases body awareness, promotes healing',
    },
    {
        'title': 'Advanced Loving Kindness',
        'description': 'Cultivate compassion and positive emotions through loving-kindness practice.',
        'difficulty': 'advanced',
        'duration_minutes': 25,
        'instructor': 'Sophia Lee',
        'meditation_type': 'Loving Kindness',
        'benefits': 'Increases compassion, improves relationships, boosts emotional wellness',
    },
]

# Create Workouts
print("Creating Workouts...")
for workout_data in workouts:
    workout, created = Workout.objects.get_or_create(**workout_data)
    if created:
        print(f"  ✓ Created: {workout.name}")
    else:
        print(f"  - Already exists: {workout.name}")

# Create Meal Plans
print("\nCreating Meal Plans...")
for meal_data in meal_plans:
    meal, created = MealPlan.objects.get_or_create(**meal_data)
    if created:
        print(f"  ✓ Created: {meal.name}")
    else:
        print(f"  - Already exists: {meal.name}")

# Create Meditations
print("\nCreating Meditations...")
for meditation_data in meditations:
    meditation, created = Meditation.objects.get_or_create(**meditation_data)
    if created:
        print(f"  ✓ Created: {meditation.title}")
    else:
        print(f"  - Already exists: {meditation.title}")

print("\n✅ Data population completed successfully!")
print("\nYou can now access the Django Admin at:")
print("http://localhost:8000/admin/")
print("\nLogin with:")
print("Username: admin")
print("Password: admin123")
