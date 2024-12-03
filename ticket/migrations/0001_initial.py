# Generated by Django 5.1.2 on 2024-10-31 08:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('date', models.DateField(verbose_name='Date')),
                ('time', models.TimeField(verbose_name='Time')),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Exam',
                'verbose_name_plural': 'Exams',
            },
        ),
        migrations.CreateModel(
            name='Grader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Grader',
                'verbose_name_plural': 'Graders',
            },
        ),
        migrations.CreateModel(
            name='ExamType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.exam', verbose_name='Exam')),
                ('grades', models.ManyToManyField(to='ticket.grader', verbose_name='Grades')),
            ],
            options={
                'verbose_name': 'Exam Type',
                'verbose_name_plural': 'Exam Types',
            },
        ),
        migrations.CreateModel(
            name='Precinct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('address', models.CharField(max_length=100, verbose_name='Address')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.exam', verbose_name='Exam')),
            ],
            options={
                'verbose_name': 'Precinct',
                'verbose_name_plural': 'Precincts',
            },
        ),
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('precinct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.precinct', verbose_name='Precinct')),
            ],
            options={
                'verbose_name': 'Floor',
                'verbose_name_plural': 'Floors',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('capacity', models.IntegerField(verbose_name='Capacity')),
                ('available_seats', models.IntegerField(verbose_name='Available Seats')),
                ('floor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.floor', verbose_name='Floor')),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=100, verbose_name='Last Name')),
                ('gender', models.CharField(choices=[('M', 'Kişi'), ('F', 'Qadın')], max_length=5, verbose_name='Gender')),
                ('school', models.CharField(max_length=100, verbose_name='School')),
                ('phone', models.CharField(max_length=100, verbose_name='Phone')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.exam', verbose_name='Exam')),
                ('exam_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.examtype', verbose_name='Exam Type')),
                ('grader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.grader', verbose_name='Grader')),
                ('precinct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.precinct', verbose_name='Precinct')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.room', verbose_name='Room')),
            ],
            options={
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
            },
        ),
    ]
