# Generated by Django 3.1.2 on 2020-11-06 03:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('costos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profesional',
            name='empresa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='profesionales', to='costos.empresa'),
        ),
    ]
