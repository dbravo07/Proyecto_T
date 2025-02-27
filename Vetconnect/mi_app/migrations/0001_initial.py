# Generated by Django 5.1 on 2024-08-15 19:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('apellido', models.CharField(max_length=255)),
                ('rut', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=20)),
                ('correo', models.EmailField(max_length=255)),
                ('direccion', models.CharField(max_length=255)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Mascota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('especie', models.CharField(max_length=255)),
                ('raza', models.CharField(max_length=255)),
                ('sexo', models.CharField(max_length=10)),
                ('peso', models.DecimalField(decimal_places=2, max_digits=5)),
                ('edad', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MedicoVeterinario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('especialidad', models.CharField(max_length=255)),
                ('correo', models.EmailField(max_length=255)),
                ('telefono', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Conversacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('ultima_actualizacion', models.DateTimeField(auto_now=True)),
                ('participantes', models.ManyToManyField(to='mi_app.medicoveterinario')),
            ],
        ),
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('motivo', models.TextField()),
                ('confirmada', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mi_app.cliente')),
                ('mascota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mi_app.mascota')),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mi_app.medicoveterinario')),
            ],
        ),
        migrations.CreateModel(
            name='MensajeConversacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.TextField()),
                ('fecha_envio', models.DateTimeField(auto_now_add=True)),
                ('leido', models.BooleanField(default=False)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mi_app.medicoveterinario')),
                ('conversacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mi_app.conversacion')),
            ],
        ),
    ]
