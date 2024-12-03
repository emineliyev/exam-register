import django_filters
from django import forms

from ticket.models import Ticket, Grader, Exam, ExamType


class TicketFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains', label="Ad", widget=forms.TextInput(
        attrs={'class': 'form-control', }))
    last_name = django_filters.CharFilter(lookup_expr='icontains', label="Soyad", widget=forms.TextInput(
        attrs={'class': 'form-control', }))
    number = django_filters.NumberFilter(lookup_expr='icontains', label="İş nömrə", widget=forms.NumberInput(
        attrs={'class': 'form-control', }))

    # Поле с выпадающим списком для выбора "Grader"
    grader = django_filters.ModelChoiceFilter(
        queryset=Grader.objects.all(),
        label="Sinif",
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )

    # Поле с выпадающим списком для выбора "Exam"
    exam = django_filters.ModelChoiceFilter(
        queryset=Exam.objects.all(),
        label="İmtahan",
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )

    # Поле с выпадающим списком для выбора "Exam Type"
    exam_type = django_filters.ModelChoiceFilter(
        queryset=ExamType.objects.all(),
        label="İmtahan növü",
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )

    class Meta:
        model = Ticket
        fields = ['number', 'first_name', 'last_name', 'grader', 'exam', 'exam_type']
