from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Workout Model
class Workout(models.Model):
    INTENSITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    intensity = models.CharField(max_length=10, choices=INTENSITY_CHOICES)
    duration_minutes = models.IntegerField(validators=[MinValueValidator(1)])
    calories_burned = models.IntegerField(validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='workouts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


# Meal Plan Model
class MealPlan(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    
    name = models.CharField(max_length=100)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    description = models.TextField()
    calories = models.IntegerField(validators=[MinValueValidator(0)])
    protein_grams = models.FloatField(validators=[MinValueValidator(0)])
    carbs_grams = models.FloatField(validators=[MinValueValidator(0)])
    fat_grams = models.FloatField(validators=[MinValueValidator(0)])
    ingredients = models.TextField()
    preparation_time = models.IntegerField(validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to='meals/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


# Meditation Session Model
class Meditation(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    duration_minutes = models.IntegerField(validators=[MinValueValidator(1)])
    instructor = models.CharField(max_length=100, blank=True)
    meditation_type = models.CharField(max_length=50, help_text="e.g., Mindfulness, Breathing, Visualization")
    benefits = models.TextField()
    audio_file = models.FileField(upload_to='meditations/', null=True, blank=True)
    image = models.ImageField(upload_to='meditation_covers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


# User Progress Tracking
class UserProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    workouts_completed = models.IntegerField(default=0)
    meditation_sessions = models.IntegerField(default=0)
    total_calories_burned = models.IntegerField(default=0)
    current_weight = models.FloatField(null=True, blank=True)
    goal_weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True, help_text="in cm")
    age = models.IntegerField(null=True, blank=True)
    daily_water_intake = models.IntegerField(default=0, help_text="in ml")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Progress"


# User Workout Assignments
class UserWorkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_workouts')
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(null=True, blank=True)
    assigned_date = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'workout')
    
    def __str__(self):
        return f"{self.user.username} - {self.workout.name}"


# User Meal Plan Assignments
class UserMealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_meal_plans')
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)
    assigned_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('user', 'meal_plan')
    
    def __str__(self):
        return f"{self.user.username} - {self.meal_plan.name}"


# User Meditation Sessions
class UserMeditation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_meditations')
    meditation = models.ForeignKey(Meditation, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(null=True, blank=True)
    assigned_date = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'meditation')
    
    def __str__(self):
        return f"{self.user.username} - {self.meditation.title}"


# Chatbot Messages
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_helpful = models.BooleanField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
