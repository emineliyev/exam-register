import random

from django.contrib.auth.models import User
from django.db import models, IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver


class Grader(models.Model):
    name = models.CharField(max_length=100, verbose_name='Sinif')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Sinif'
        verbose_name_plural = 'Siniflər'


class Exam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User", related_name='exam')
    name = models.CharField(max_length=100, verbose_name="Ad")
    date = models.DateField(verbose_name="Tarix")
    time = models.TimeField(verbose_name="Saat")
    status = models.BooleanField(default=False, verbose_name="Status")
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['order']
        verbose_name = 'Imtahan'
        verbose_name_plural = 'Imtahanlar'


class ExamType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ad")
    grades = models.ManyToManyField(Grader, verbose_name="Siniflər")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name="İmtahan")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'İmtahan növü'
        verbose_name_plural = 'İmtahan növü'


class Precinct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User", related_name="precincts")
    name = models.CharField(max_length=100, verbose_name="Ad")
    address = models.CharField(max_length=100, verbose_name="Ünvan")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name="İmtahan")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Məntəqə'
        verbose_name_plural = 'Məntəqələr'


class Floor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User", related_name="floor")
    name = models.CharField(max_length=100, verbose_name="Mərtəbə adı")
    precinct = models.ForeignKey(Precinct, on_delete=models.CASCADE, verbose_name="Məntəqə")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Mərtəbə'
        verbose_name_plural = 'Mərtəbələr'


class Room(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ad")
    capacity = models.IntegerField(verbose_name="Yer sayı")
    available_seats = models.IntegerField(verbose_name="Böş yer sayı", default=0)
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, verbose_name="İmtahan növü")
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, verbose_name="Mərtəbə")

    def save(self, *args, **kwargs):
        if not self.available_seats:
            self.available_seats = self.capacity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Otaq'
        verbose_name_plural = 'Otaqlar'


class Seat(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.PositiveIntegerField()

    def __str__(self):
        return f"Room {self.room.name} - Seat {self.seat_number}"

    class Meta:
        unique_together = ('room', 'seat_number')


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Sahib", related_name="tickets")
    number = models.IntegerField(default=0, blank=True, null=True, verbose_name='İş nömrə')
    first_name = models.CharField(max_length=100, verbose_name="Ad")
    last_name = models.CharField(max_length=100, verbose_name="Soyad")
    grader = models.ForeignKey(Grader, on_delete=models.CASCADE, verbose_name="Sinif")
    gender = models.CharField(choices=(('M', 'Kişi'), ('F', 'Qadın')), max_length=5, verbose_name="Cinsiyyət")
    school = models.CharField(max_length=100, verbose_name="Məktəb")
    phone = models.CharField(max_length=100, verbose_name="Telefon")
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE, verbose_name="İmtahan")
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, verbose_name="İmtahan növü")
    precinct = models.ForeignKey(Precinct, on_delete=models.CASCADE, verbose_name="Məntəqə")
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, verbose_name='Mərtəbə')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Otaq")
    seat_number = models.IntegerField(null=True, blank=True, verbose_name="Yer nömrəsi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Qeydiyyat tarixi')

    def save(self, *args, **kwargs):
        if not self.seat_number:
            raise ValueError("Seat must be selected")

        if not self.number:
            for _ in range(10):  # Даем 10 попыток
                self.number = random.randint(200000, 9999999)
                if not Ticket.objects.filter(number=self.number).exists():
                    break
            else:
                raise ValueError("Не удалось сгенерировать уникальный номер билета")

        if self.room.available_seats > 0:
            self.room.available_seats -= 1
            self.room.save()
            super().save(*args, **kwargs)
        else:
            raise ValueError("Room is empty")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Bilet'
        verbose_name_plural = 'Biletlər'
        ordering = ['-created_at']


@receiver(post_save, sender=Room)
def create_seats_for_room(sender, instance, created, **kwargs):
    if created:  # Проверяем, что комната была создана, а не обновлена
        for seat_number in range(1, instance.capacity + 1):
            Seat.objects.create(room=instance, seat_number=seat_number)
