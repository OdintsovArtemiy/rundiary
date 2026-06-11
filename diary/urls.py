from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('workout/add/', views.workout_add, name='workout_add'),
    path('goals/', views.goals, name='goals'),
    path('goals/add/', views.goal_add, name='goal_add'),
]