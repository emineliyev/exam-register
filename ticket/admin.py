from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin

from .models import (
    Grader,
    Exam,
    ExamType,
    Precinct,
    Floor,
    Room,
    Ticket,
)


@admin.register(Grader)
class GraderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Exam)
class ExamAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'order')


@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Precinct)
class PrecinctAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')
    list_display_links = ('id', 'first_name')
    list_filter = ('exam_type', 'exam')
    search_fields = ('first_name', 'last_name')
