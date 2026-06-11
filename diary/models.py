from django.db import models
from django.contrib.auth.models import User


class Athlete(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='athlete', verbose_name='Пользователь')
    birth_year = models.PositiveIntegerField(verbose_name='Год рождения')
    resting_hr = models.PositiveIntegerField(verbose_name='Пульс покоя')
    max_hr = models.PositiveIntegerField(verbose_name='Максимальный пульс')
    weight = models.PositiveIntegerField(verbose_name='Вес (кг)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Атлет'
        verbose_name_plural = 'Атлеты'

    def __str__(self):
        return f"Athlete {self.user.username}"


class TrainingGoal(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name='goals', verbose_name='Атлет')
    title = models.CharField(max_length=200, verbose_name='Название')
    target_distance_km = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Целевая дистанция (км)')
    target_date = models.DateField(verbose_name='Целевая дата')
    target_pace_min_per_km = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Целевой темп (мин/км)')
    is_active = models.BooleanField(default=True, verbose_name='Активная')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Цель тренировок'
        verbose_name_plural = 'Цели тренировок'

    def __str__(self):
        return self.title


class Workout(models.Model):
    WORKOUT_TYPES = [
        ('easy', 'Лёгкая'),
        ('tempo', 'Темповая'),
        ('interval', 'Интервальная'),
        ('long', 'Длинная'),
        ('recovery', 'Восстановительная'),
    ]

    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name='workouts', verbose_name='Атлет')
    goal = models.ForeignKey(TrainingGoal, on_delete=models.SET_NULL, null=True, blank=True, related_name='workouts', verbose_name='Цель')
    date = models.DateField(verbose_name='Дата')
    distance_km = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Дистанция (км)')
    duration_minutes = models.PositiveIntegerField(verbose_name='Время (минуты)')
    avg_heart_rate = models.PositiveIntegerField(verbose_name='Средний пульс')
    workout_type = models.CharField(max_length=20, choices=WORKOUT_TYPES, verbose_name='Тип тренировки')
    notes = models.TextField(blank=True, verbose_name='Заметки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ['-date']
        verbose_name = 'Тренировка'
        verbose_name_plural = 'Тренировки'

    def __str__(self):
        return f"{self.date} - {self.distance_km} km"

    @property
    def pace(self):
        if self.distance_km == 0:
            return "0:00"
        total_seconds = float(self.duration_minutes) * 60 / float(self.distance_km)
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        return f"{minutes}:{seconds:02d}"

    @property
    def pulse_zone(self):
        if not self.athlete.max_hr:
            return "—"
        percent = self.avg_heart_rate / self.athlete.max_hr * 100
        if percent < 60:
            return "Z1"
        elif percent < 70:
            return "Z2"
        elif percent < 80:
            return "Z3"
        elif percent < 90:
            return "Z4"
        else:
            return "Z5"