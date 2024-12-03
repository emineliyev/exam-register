from django.http import JsonResponse, request, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
import openpyxl
from ticket.filters import TicketFilter
from ticket.forms import CreateTicketForm
from ticket.models import Ticket, Floor, Room, ExamType, Precinct, Exam
import logging

logger = logging.getLogger(__name__)


class TicketListView(ListView):
    model = Ticket
    template_name = 'ticket/index.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = TicketFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context


def load_exam_type(request):
    exam = request.GET.get('exam')
    exam_typs = ExamType.objects.filter(exam=exam).values('id', 'name')
    return JsonResponse(list(exam_typs), safe=False)


def load_precinct(request):
    exam = request.GET.get('exam')
    precincts = Precinct.objects.filter(exam=exam).values('id', 'name')
    return JsonResponse(list(precincts), safe=False)


def load_floor(request):
    precinct_id = request.GET.get('precinct_id')
    floors = Floor.objects.filter(precinct_id=precinct_id).values('id', 'name')
    return JsonResponse(list(floors), safe=False)


def load_room(request):
    floor_id = request.GET.get('floor_id')
    exam_type_id = request.GET.get('exam_type')

    # Фильтруем по переданным параметрам
    rooms = Room.objects.all()

    if floor_id:
        rooms = rooms.filter(floor_id=floor_id)
    if exam_type_id:
        rooms = rooms.filter(exam_type_id=exam_type_id)

    # Преобразуем результат в JSON
    rooms = rooms.values('id', 'name')
    return JsonResponse(list(rooms), safe=False)


def load_seats(request):
    room_id = request.GET.get('room_id')

    if not room_id:
        return JsonResponse({'error': 'room_id parameter is missing'}, status=400)

    try:
        room = get_object_or_404(Room, id=room_id)
        total_seats = room.capacity
        occupied_seats = Ticket.objects.filter(room=room).values_list('seat_number', flat=True)

        seats = [{"seat_number": i, "occupied": i in occupied_seats} for i in range(1, total_seats + 1)]
        return JsonResponse(seats, safe=False)

    except Exception as e:
        # Добавление отладочного вывода
        print(f"Error loading seats: {e}")
        return JsonResponse({'error': 'Internal Server Error'}, status=500)


class CreateTicketView(CreateView):
    model = Ticket
    form_class = CreateTicketForm
    template_name = 'ticket/add-ticket.html'
    success_url = reverse_lazy('ticket:index')

    def form_valid(self, form):
        seat_number = form.cleaned_data.get('seat_number')
        if not seat_number:
            form.add_error('seat_number', 'Seat must be selected')
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class TicketUpdate(UpdateView):
    model = Ticket
    form_class = CreateTicketForm
    template_name = 'ticket/update.html'
    success_url = reverse_lazy('ticket:update')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = self.object

        context['form'].fields['exam_type'].initial = ticket.exam_type
        context['form'].fields['precinct'].initial = ticket.precinct
        context['form'].fields['floor'].initial = ticket.floor
        context['form'].fields['room'].initial = ticket.room
        context['form'].fields['seat_number'].initial = ticket.seat_number

        return context


def get_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    context = {
        'ticket': ticket,
    }
    return render(request, 'ticket/ticket.html', context=context)


def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    ticket.delete()
    return render(request, 'ticket/index.html')


def get_report(request):
    exams = Exam.objects.all()
    context = {
        'exams': exams
    }
    return render(request, 'ticket/report.html', context=context)


def load_exam_type_report(request):
    exam = request.GET.get('exam')
    exam_typs = ExamType.objects.filter(exam=exam).values('id', 'name')
    return JsonResponse(list(exam_typs), safe=False)


def export_to_excel(request):
    exam_id = request.GET.get('exam')
    exam_type_id = request.GET.get('exam_type')

    if not exam_id or not exam_type_id:
        return HttpResponse("Heç bir imtahan və ya imtahan növü seçilməyib.", status=400)

    tickets = Ticket.objects.filter(exam_id=exam_id, exam_type_id=exam_type_id).select_related('room')

    workbook = openpyxl.Workbook()
    workbook.remove(workbook.active)

    if not tickets.exists():

        sheet = workbook.create_sheet(title="Məlumat yoxdur")
        sheet.append(["Seçilmiş imtahan və imtahan növü üçün heç bir məlumat yoxdur."])
    else:

        rooms = tickets.values_list('room', flat=True).distinct()
        for room_id in rooms:
            room = Room.objects.get(id=room_id)
            room_tickets = tickets.filter(room=room)

            sheet = workbook.create_sheet(title=f"OTAQ {room.name}")

            sheet.append(['İş nömrə', 'Ad', 'Soyad', 'Sinif', 'Cins', 'Məktəb', 'Telefon', 'İmtahan növü', 'Yer'])

            for ticket in room_tickets:
                sheet.append([
                    ticket.number,
                    ticket.first_name,
                    ticket.last_name,
                    str(ticket.grader),
                    'Kişi' if ticket.gender == 'M' else 'Qadın',
                    ticket.school,
                    ticket.phone,
                    str(ticket.exam_type),
                    ticket.seat_number,
                ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=İmtahan.xlsx'
    workbook.save(response)

    return response
