from django.contrib import admin
from .models import (
    Workout, MealPlan, Meditation, UserProgress,
    UserWorkout, UserMealPlan, UserMeditation, ChatMessage
)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'intensity', 'duration_minutes', 'calories_burned', 'created_at')
    list_filter = ('intensity', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'intensity')
        }),
        ('Workout Details', {
            'fields': ('duration_minutes', 'calories_burned', 'image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'meal_type', 'calories', 'preparation_time', 'created_at')
    list_filter = ('meal_type', 'created_at')
    search_fields = ('name', 'description', 'ingredients')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'meal_type', 'description', 'image')
        }),
        ('Nutrition Information', {
            'fields': ('calories', 'protein_grams', 'carbs_grams', 'fat_grams')
        }),
        ('Recipe Details', {
            'fields': ('ingredients', 'preparation_time')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Meditation)
class MeditationAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'duration_minutes', 'meditation_type', 'created_at')
    list_filter = ('difficulty', 'meditation_type', 'created_at')
    search_fields = ('title', 'description', 'benefits')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'difficulty', 'meditation_type', 'image')
        }),
        ('Session Details', {
            'fields': ('duration_minutes', 'instructor', 'benefits')
        }),
        ('Media', {
            'fields': ('audio_file',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'workouts_completed', 'meditation_sessions', 'total_calories_burned', 'updated_at')
    list_filter = ('updated_at', 'user')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Fitness Metrics', {
            'fields': ('workouts_completed', 'meditation_sessions', 'total_calories_burned', 'daily_water_intake')
        }),
        ('Physical Measurements', {
            'fields': ('current_weight', 'goal_weight', 'height', 'age')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserWorkout)
class UserWorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'workout', 'completed', 'assigned_date', 'completed_date')
    list_filter = ('completed', 'assigned_date', 'completed_date')
    search_fields = ('user__username', 'workout__name')
    readonly_fields = ('assigned_date',)
    fieldsets = (
        ('Assignment', {
            'fields': ('user', 'workout', 'assigned_date')
        }),
        ('Completion Status', {
            'fields': ('completed', 'completed_date')
        }),
    )


@admin.register(UserMealPlan)
class UserMealPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal_plan', 'is_active', 'assigned_date')
    list_filter = ('is_active', 'assigned_date')
    search_fields = ('user__username', 'meal_plan__name')
    readonly_fields = ('assigned_date',)
    fieldsets = (
        ('Assignment', {
            'fields': ('user', 'meal_plan', 'assigned_date')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(UserMeditation)
class UserMeditationAdmin(admin.ModelAdmin):
    list_display = ('user', 'meditation', 'completed', 'assigned_date', 'completed_date')
    list_filter = ('completed', 'assigned_date', 'completed_date')
    search_fields = ('user__username', 'meditation__title')
    readonly_fields = ('assigned_date',)
    fieldsets = (
        ('Assignment', {
            'fields': ('user', 'meditation', 'assigned_date')
        }),
        ('Completion Status', {
            'fields': ('completed', 'completed_date')
        }),
    )


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'is_helpful')
    list_filter = ('timestamp', 'is_helpful')
    search_fields = ('user__username', 'message', 'response')
    readonly_fields = ('timestamp',)
    fieldsets = (
        ('User & Timestamp', {
            'fields': ('user', 'timestamp')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Response', {
            'fields': ('response',)
        }),
        ('Feedback', {
            'fields': ('is_helpful',)
        }),
    )
