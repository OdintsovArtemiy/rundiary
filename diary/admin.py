from django.contrib import admin
from .models import Athlete, Workout, TrainingGoal


@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_year', 'resting_hr', 'max_hr', 'weight')
    search_fields = ('user__username',)


@admin.register(TrainingGoal)
class TrainingGoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'athlete', 'target_distance_km', 'target_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('date', 'athlete', 'distance_km', 'duration_minutes', 'workout_type', 'avg_heart_rate')
    list_filter = ('workout_type', 'date')
    search_fields = ('athlete__user__username',)