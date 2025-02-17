from django import forms
from .models import Ticket, Precinct, Exam, Room, Floor, Grader, ExamType
from django_select2.forms import Select2MultipleWidget


class CreateTicketForm(forms.ModelForm):
    seat_number = forms.IntegerField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Ticket
        fields = [
            'first_name', 'last_name', 'grader', 'gender', 'school',
            'phone', 'exam', 'exam_type', 'precinct', 'floor', 'room', 'seat_number'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'grader': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'school': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'exam': forms.Select(attrs={'class': 'form-control', 'id': 'examSelect'}),
            'exam_type': forms.Select(attrs={'class': 'form-control', 'id': 'examTypeSelect'}),
            'precinct': forms.Select(attrs={'class': 'form-control', 'id': 'precinctSelect'}),
            'floor': forms.Select(attrs={'class': 'form-control', 'id': 'floorSelect'}),
            'room': forms.Select(attrs={'class': 'form-control', 'id': 'roomSelect'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['exam'].queryset = Exam.objects.filter(user=user)

            if 'exam' in self.data:
                try:
                    exam_id = int(self.data.get('exam'))
                    self.fields['precinct'].queryset = Precinct.objects.filter(exam_id=exam_id)
                    self.fields['floor'].queryset = Floor.objects.filter(precinct__exam_id=exam_id)
                    self.fields['room'].queryset = Room.objects.filter(exam_type__exam_id=exam_id)  # ✅ Исправлено
                    self.fields['exam_type'].queryset = ExamType.objects.filter(exam_id=exam_id)
                except (ValueError, TypeError):
                    pass  # Если данные некорректные, оставляем пустые списки
            else:
                self.fields['precinct'].queryset = Precinct.objects.none()
                self.fields['room'].queryset = Room.objects.none()
                self.fields['floor'].queryset = Floor.objects.none()
                self.fields['exam_type'].queryset = ExamType.objects.none()


class CreateExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'date', 'time', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(format='%H:%M', attrs={'class': 'form-control', 'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['date'].initial = self.instance.date.strftime('%Y-%m-%d')
            self.fields['time'].initial = self.instance.time.strftime('%H:%M')


class CreateExamTypeForm(forms.ModelForm):
    class Meta:
        model = ExamType
        fields = ['name', 'grades', 'exam']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'grades': Select2MultipleWidget(attrs={'class': 'form-control'}),
            'exam': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Извлекаем пользователя и удаляем из kwargs
        super().__init__(*args, **kwargs)

        if user:
            # Фильтруем экзамены, чтобы пользователь видел только свои
            self.fields['exam'].queryset = Exam.objects.filter(user=user)


class CreatePrecinctForm(forms.ModelForm):
    class Meta:
        model = Precinct
        fields = ['name', 'address', 'exam']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'exam': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Извлекаем пользователя и удаляем из kwargs
        super().__init__(*args, **kwargs)

        if user:
            # Фильтруем экзамены, чтобы пользователь видел только свои
            self.fields['exam'].queryset = Exam.objects.filter(user=user)


class FloorCreateForm(forms.ModelForm):
    class Meta:
        model = Floor
        fields = [
            'name',
            'precinct'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'precinct': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['precinct'].queryset = Precinct.objects.filter(user=user)


class RoomCreateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'name',
            'capacity',
            'available_seats',
            'exam_type',
            'floor',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'available_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'exam_type': forms.Select(attrs={'class': 'form-control'}),
            'floor': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # ✅ Извлекаем пользователя
        super().__init__(*args, **kwargs)

        if user:
            # ✅ Фильтруем `Floor` по пользователю
            self.fields['floor'].queryset = Floor.objects.filter(user=user)

            # ✅ Фильтруем `exam_type`, показывая только экзамены пользователя
            self.fields['exam_type'].queryset = ExamType.objects.filter(exam__user=user)
