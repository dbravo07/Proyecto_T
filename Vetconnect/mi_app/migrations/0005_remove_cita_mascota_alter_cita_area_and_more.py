# Generated by Django 5.1 on 2024-08-16 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mi_app', '0004_veterinario_remove_cita_confirmada_cita_area_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cita',
            name='mascota',
        ),
        migrations.AlterField(
            model_name='cita',
            name='area',
            field=models.CharField(choices=[('Control', 'Control'), ('Consulta', 'Consulta'), ('Procedimiento', 'Procedimiento')], max_length=20),
        ),
        migrations.AlterField(
            model_name='cita',
            name='especialidad',
            field=models.CharField(max_length=100),
        ),
    ]
