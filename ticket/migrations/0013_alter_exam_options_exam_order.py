# Generated by Django 5.1.2 on 2024-11-10 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0012_remove_ticket_seat_ticket_seat_number_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exam',
            options={'ordering': ['order'], 'verbose_name': 'Imtahan', 'verbose_name_plural': 'Imtahanlar'},
        ),
        migrations.AddField(
            model_name='exam',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
