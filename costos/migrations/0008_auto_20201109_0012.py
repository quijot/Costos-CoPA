# Generated by Django 3.1.2 on 2020-11-09 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costos', '0007_auto_20201108_2352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instrumento',
            name='cantidad_de_trabajos',
        ),
        migrations.AlterField(
            model_name='instrumento',
            name='vida_util',
            field=models.PositiveIntegerField(default=5, help_text='Vida útil esperada en jornadas de medición.', verbose_name='vida útil'),
        ),
    ]