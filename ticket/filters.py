import django_filters
from django import forms
from .models import Ticket, Grader, Exam, ExamType


class TicketFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains', label="Ad", widget=forms.TextInput(
        attrs={'class': 'form-control', }))
    last_name = django_filters.CharFilter(lookup_expr='icontains', label="Soyad", widget=forms.TextInput(
        attrs={'class': 'form-control', }))
    number = django_filters.NumberFilter(lookup_expr='icontains', label="İş nömrə", widget=forms.NumberInput(
        attrs={'class': 'form-control', }))

    grader = django_filters.ModelChoiceFilter(
        queryset=Grader.objects.all(),
        label="Sinif",
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )

    exam = django_filters.ModelChoiceFilter(
        queryset=Exam.objects.none(),  # ❌ Начинаем с пустого списка
        label="İmtahan",
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )

    exam_type = django_filters.ModelChoiceFilter(
        queryset=ExamType.objects.none(), # ❌ Начинаем с пустого списка
        label="İmtahan növü",
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )

    class Meta:
        model = Ticket
        fields = ['number', 'first_name', 'last_name', 'grader', 'exam', 'exam_type']

    def __init__(self, *args, **kwargs):
        """Фильтруем экзамены по текущему пользователю"""
        user = kwargs.pop('user', None)  # Извлекаем `user` из `kwargs`
        super().__init__(*args, **kwargs)

        if user:
            self.filters['exam'].queryset = Exam.objects.filter(user=user)  # ✅ Фильтруем `Exam`
            self.filters['exam_type'].queryset = ExamType.objects.filter(user=user)  # ✅ Фильтруем `Exam`
