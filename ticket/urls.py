from django.urls import path
from .views import TicketListView, CreateTicketView, get_ticket, load_exam_type, load_precinct, load_floor, load_room, \
    load_seats, delete_ticket, TicketUpdate, get_report, load_exam_type_report, export_to_excel

app_name = 'ticket'

urlpatterns = [
    path('', TicketListView.as_view(), name='index'),
    path('add-ticket/', CreateTicketView.as_view(), name='add-ticket'),
    path('load_exam_type/', load_exam_type, name='load_exam_type'),
    path('load_precinct/', load_precinct, name='load_precinct'),
    path('load_floor/', load_floor, name='load_floor'),
    path('load_room/', load_room, name='load_room'),
    path('load_seats/', load_seats, name='load_seats'),
    path('ticket/<int:ticket_id>/', get_ticket, name='ticket'),
    path('update/<int:pk>/', TicketUpdate.as_view(), name='update'),
    path('delete_ticket/<int:ticket_id>/', delete_ticket, name='delete_ticket'),
    path('load_exam_type_report/', load_exam_type_report, name='load_exam_type_report'),
    path('report/', get_report, name='report'),
    path('export_to_excel/', export_to_excel, name='export_to_excel'),
]