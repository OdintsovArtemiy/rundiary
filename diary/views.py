from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import pandas as pd
import plotly.express as px
from .forms import RegisterForm, WorkoutForm, TrainingGoalForm
from .models import Athlete, Workout


def home(request):
    return render(request, 'diary/home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            birth_year = form.cleaned_data['birth_year']
            Athlete.objects.create(
                user=user,
                birth_year=birth_year,
                resting_hr=form.cleaned_data['resting_hr'],
                max_hr=220 - (2026 - birth_year),
                weight=form.cleaned_data['weight'],
            )
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'diary/register.html', {'form': form})


@login_required
def dashboard(request):
    athlete = request.user.athlete
    workouts = athlete.workouts.all()

    chart_weekly = None
    chart_pace = None
    chart_zones = None
    stats_table = None

    if workouts.exists():
        data = [{
            'date': w.date,
            'distance_km': float(w.distance_km),
            'duration_minutes': w.duration_minutes,
            'avg_heart_rate': w.avg_heart_rate,
            'workout_type': w.get_workout_type_display(),
            'pace_min_per_km': float(w.duration_minutes) / float(w.distance_km),
            'pulse_zone': w.pulse_zone,
        } for w in workouts]

        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])

        weekly = df.groupby(pd.Grouper(key='date', freq='W'))['distance_km'].sum().reset_index()
        weekly.columns = ['Week', 'Km']
        fig1 = px.bar(weekly, x='Week', y='Km', title='Weekly volume (km)')
        chart_weekly = fig1.to_html(full_html=False, include_plotlyjs='cdn')

        df_sorted = df.sort_values('date')
        fig2 = px.line(df_sorted, x='date', y='pace_min_per_km', title='Pace trend (min/km)', markers=True)
        chart_pace = fig2.to_html(full_html=False, include_plotlyjs=False)

        zones = df['pulse_zone'].value_counts().reset_index()
        zones.columns = ['Zone', 'Count']
        fig3 = px.pie(zones, names='Zone', values='Count', title='Pulse zones distribution')
        chart_zones = fig3.to_html(full_html=False, include_plotlyjs=False)

        stats = df.groupby('workout_type').agg(
            count=('distance_km', 'count'),
            total_km=('distance_km', 'sum'),
            avg_pace=('pace_min_per_km', 'mean'),
            avg_hr=('avg_heart_rate', 'mean'),
        ).round(2).reset_index()
        stats.columns = ['Type', 'Count', 'Total km', 'Avg pace', 'Avg HR']
        stats_table = stats.to_html(classes='table table-striped', index=False)

    return render(request, 'diary/dashboard.html', {
        'athlete': athlete,
        'workouts': workouts,
        'chart_weekly': chart_weekly,
        'chart_pace': chart_pace,
        'chart_zones': chart_zones,
        'stats_table': stats_table,
    })


@login_required
def workout_add(request):
    athlete = request.user.athlete
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.athlete = athlete
            workout.save()
            return redirect('dashboard')
    else:
        form = WorkoutForm()
    return render(request, 'diary/workout_form.html', {'form': form})


@login_required
def goals(request):
    athlete = request.user.athlete
    goals_list = athlete.goals.all().order_by('-is_active', '-target_date')
    return render(request, 'diary/goals.html', {'goals_list': goals_list})


@login_required
def goal_add(request):
    athlete = request.user.athlete
    if request.method == 'POST':
        form = TrainingGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.athlete = athlete
            goal.save()
            return redirect('goals')
    else:
        form = TrainingGoalForm()
    return render(request, 'diary/goal_form.html', {'form': form})