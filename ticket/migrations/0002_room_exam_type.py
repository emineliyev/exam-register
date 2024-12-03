# Generated by Django 5.1.2 on 2024-10-31 08:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='exam_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ticket.examtype', verbose_name='Exam Type'),
            preserve_default=False,
        ),
    ]