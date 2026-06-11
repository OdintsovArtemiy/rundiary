from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Workout, Athlete


class RegisterForm(UserCreationForm):
    birth_year = forms.IntegerField(min_value=1900, max_value=2020, label='Год рождения')
    resting_hr = forms.IntegerField(min_value=30, max_value=120, label='Пульс покоя')
    weight = forms.IntegerField(min_value=30, max_value=200, label='Вес (кг)')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'birth_year', 'resting_hr', 'weight')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ('date', 'distance_km', 'duration_minutes', 'avg_heart_rate', 'workout_type', 'notes')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_distance_km(self):
        distance = self.cleaned_data['distance_km']
        if distance <= 0:
            raise forms.ValidationError('Дистанция должна быть больше 0')
        return distance

    def clean_avg_heart_rate(self):
        hr = self.cleaned_data['avg_heart_rate']
        if hr < 40 or hr > 220:
            raise forms.ValidationError('Пульс должен быть от 40 до 220')
        return hr