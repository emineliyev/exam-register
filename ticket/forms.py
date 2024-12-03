from django import forms

from ticket.models import Ticket


class CreateTicketForm(forms.ModelForm):
    seat_number = forms.IntegerField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Ticket
        fields = [
            'first_name',
            'last_name',
            'grader',
            'gender',
            'school',
            'phone',
            'exam',
            'exam_type',
            'precinct',
            'floor',
            'room',
            'seat_number',
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
