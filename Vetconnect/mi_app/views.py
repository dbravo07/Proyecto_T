from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .forms import SolicitarCitaForm, RegistroMedicoForm, EditarMascotaForm, AgregarObservacionForm
from django.db import models
from .models import Mascota, Cita, Cliente, MedicoVeterinario, Conversacion, RegistroMedico, Observacion
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout as auth_logout
from datetime import datetime
from datetime import time

# Vista de la página de inicio


def index(request):
    return render(request, 'index.html')

# Vista para mostrar el formulario de creación de usuario


def crear_usuario(request):
    return render(request, 'registrate.html')

# Vista para manejar el registro de nuevos usuarios


def ingresar_usuario(request):
    if request.method == 'POST':
        correo = request.POST['correo']

        # Verificar si el correo ya existe en la base de datos
        if Cliente.objects.filter(correo=correo).exists():
            return render(request, 'registrate.html', {'error': 'El correo ya está registrado. Por favor, usa otro correo.'})

        # Crear un nuevo cliente si el correo es único
        cliente = Cliente(
            nombre=request.POST['nombre'],
            apellido=request.POST['apellido'],
            rut=request.POST['rut'],
            telefono=request.POST['telefono'],
            correo=correo,
            direccion=request.POST['direccion'],
            # Encriptar la contraseña
            password=make_password(request.POST['password'])
        )
        cliente.save()
        # Redirigir a la página principal después del registro
        return redirect('index')

    return render(request, 'registrate.html')

# Vista para mostrar y editar el perfil del usuario


def perfil_usuario(request):
    cliente = request.session.get('cliente', None)
    if cliente:
        cliente = Cliente.objects.get(id=cliente['id'])
    return render(request, 'perfil.html', {'cliente': cliente})

# Vista para editar el perfil del usuario


def editar_perfil(request):
    cliente = Cliente.objects.get(id=request.session['cliente']['id'])
    if request.method == 'POST':
        # Actualizar los campos del perfil del cliente
        cliente.nombre = request.POST['nombre']
        cliente.apellido = request.POST['apellido']
        cliente.correo = request.POST['correo']
        cliente.direccion = request.POST['direccion']

        # Verifica que el correo no esté ya en uso por otro usuario
        if not Cliente.objects.filter(correo=cliente.correo).exclude(id=cliente.id).exists():
            cliente.save()
            request.session['cliente'] = {
                'id': cliente.id, 'nombre': cliente.nombre, 'correo': cliente.correo}
            # Redirigir al perfil después de guardar cambios
            return redirect('perfil_usuario')
        else:
            return render(request, 'editar_perfil.html', {'cliente': cliente, 'error': 'El correo ya está en uso.'})
    return render(request, 'editar_perfil.html', {'cliente': cliente})

# Vista para la interfaz principal después del login


def interfaz(request):
    if 'cliente' not in request.session:
        # Redirigir al login si no hay un cliente en la sesión
        return redirect('login')

    citas = Cita.objects.all()  # Obtener todas las citas
    mascotas = Mascota.objects.all()  # Obtener todas las mascotas
    veterinarios = MedicoVeterinario.objects.all()  # Obtener todos los veterinarios
    cliente = request.session.get('cliente', None)

    return render(request, 'interfaz.html', {
        'mascotas': mascotas,
        'veterinarios': veterinarios,
        'citas': citas,
        'cliente': cliente
    })

# Vista para ingresar una nueva mascota


def ingresar_mascota_view(request):
    if request.method == 'POST':
        # Obtener el cliente desde la sesión
        cliente_id = request.session.get('cliente', {}).get('id')
        if not cliente_id:
            return redirect('login')

        cliente = Cliente.objects.get(id=cliente_id)

        # Obtener los datos de la mascota desde el formulario
        nombre = request.POST.get('nombre')
        especie = request.POST.get('especie')
        raza = request.POST.get('raza')
        sexo = request.POST.get('sexo')
        edad = request.POST.get('edad')
        peso = request.POST.get('peso')

        # Crear y guardar la nueva mascota asociada al cliente
        nueva_mascota = Mascota(
            nombre=nombre,
            especie=especie,
            raza=raza,
            sexo=sexo,
            edad=edad,
            peso=peso,
            cliente=cliente  # Asociar la mascota al cliente
        )
        nueva_mascota.save()

        # Redirigir a la interfaz principal después de guardar
        return redirect('interfaz')

    return render(request, 'ingresar_mascota.html')


# Vista para ver las mascotas de un cliente


def ver_mascotas_view(request):
    cliente_id = request.session.get('cliente', {}).get('id')

    if cliente_id:
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            mascotas = Mascota.objects.filter(cliente=cliente)
            print(mascotas)  # Agrega esta línea para depurar
        except Cliente.DoesNotExist:
            return redirect('login')

        return render(request, 'ver_mascotas.html', {'mascotas': mascotas})
    else:
        return redirect('login')


# Vista para eliminar una mascota específica


def eliminar_mascota_view(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    mascota.delete()  # Eliminar la mascota
    # Redirigir a la lista de mascotas después de eliminar
    return redirect('ver_mascotas')

# Vista para guardar una nueva mascota o actualizar una existente


def guardar_mascota(request, mascota_id=None):
    if request.method == 'POST':
        # Obtener el cliente desde la sesión
        cliente_id = request.session.get('cliente', {}).get('id')
        if not cliente_id:
            # Redirigir al login si no hay cliente en la sesión
            return redirect('login')

        cliente = Cliente.objects.get(id=cliente_id)

        if mascota_id:
            # Si mascota_id está presente, actualizar la mascota existente
            mascota = get_object_or_404(Mascota, id=mascota_id)
        else:
            # Si no, crear una nueva mascota
            mascota = Mascota(cliente=cliente)  # Asociar la mascota al cliente

        # Actualizar o asignar valores a la mascota
        mascota.nombre = request.POST.get('nombre')
        mascota.especie = request.POST.get('especie')
        mascota.raza = request.POST.get('raza')
        mascota.sexo = request.POST.get('sexo')
        mascota.edad = request.POST.get('edad')
        mascota.peso = request.POST.get('peso')

        try:
            mascota.save()  # Guardar la mascota (nueva o actualizada)
        except Exception as e:
            return render(request, 'interfaz.html', {'error': str(e)})

        # Redirigir a la interfaz principal después de guardar
        return redirect('interfaz')

    return render(request, 'interfaz.html')

# Vista para editar una mascota existente


def editar_mascota_view(request, mascota_id):
    # Obtener la mascota por su ID
    mascota = get_object_or_404(Mascota, id=mascota_id)

    if request.method == 'POST':
        # Actualizar los campos de la mascota con los datos proporcionados en el formulario
        mascota.nombre = request.POST.get('nombre')
        mascota.especie = request.POST.get('especie')
        mascota.raza = request.POST.get('raza')
        mascota.sexo = request.POST.get('sexo')
        mascota.edad = request.POST.get('edad')
        mascota.peso = request.POST.get('peso')

        mascota.save()  # Guardar los cambios en la base de datos
        # Redirigir a la lista de mascotas después de guardar
        return redirect('ver_mascotas')

    # Mostrar el formulario de edición
    return render(request, 'editar_mascota.html', {'mascota': mascota})

# Vista para solicitar una nueva cita


def solicitar_cita_view(request):
    if request.method == 'POST':
        form = SolicitarCitaForm(
            request.POST, cliente_id=request.session['cliente']['id'])

        if form.is_valid():
            cita = form.save(commit=False)
            cita.cliente_id = request.session['cliente']['id']

            if Cita.objects.filter(hora=cita.hora, fecha=cita.fecha, medico=cita.medico).exists():
                form.add_error('hora', 'La hora seleccionada ya está ocupada.')
            else:
                cita.hora_seleccionada = True
                try:
                    cita.save()
                    return redirect('interfaz')
                except Exception as e:
                    form.add_error(None, f"Error al guardar la cita: {str(e)}")
        else:
            print(form.errors)
    else:
        form = SolicitarCitaForm(cliente_id=request.session['cliente']['id'])

    medico = form['medico'].value()  # Obtener el médico seleccionado
    fecha = form['fecha'].value()  # Obtener la fecha seleccionada

    horas_ocupadas = []
    if medico and fecha:
        horas_ocupadas = Cita.objects.filter(
            medico=medico, fecha=fecha).values_list('hora', flat=True)

    horas = [(f"{h:02}:00", f"{h:02}:00")
             for h in range(9, 18) if f"{h:02}:00" not in horas_ocupadas]
    form.fields['hora'].choices = horas

    return render(request, 'solicitar_cita.html', {
        'form': form,
        'horas_ocupadas': horas_ocupadas,
        'horas': horas
    })

# Vista para guardar una cita


def guardar_cita_view(request):
    if request.method == 'POST':
        form = SolicitarCitaForm(request.POST)

        if form.is_valid():
            cita = form.save(commit=False)
            cita.cliente_id = request.session['cliente']['id']
            cita.save()

            return redirect('interfaz')
        else:
            return render(request, 'solicitar_cita.html', {'form': form})
    else:
        return redirect('solicitar_cita')

# Vista para ver las próximas citas del cliente


def proximas_citas_view(request):
    if 'cliente' not in request.session:
        return redirect('login')

    citas = Cita.objects.filter(
        cliente_id=request.session['cliente']['id']).order_by('fecha', 'hora')
    return render(request, 'proximas_citas.html', {'citas': citas})

# Vista para ver la ficha de una mascota


def ficha_mascota_view(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    observaciones = mascota.observaciones.all()

    if request.method == 'POST':
        form_mascota = EditarMascotaForm(request.POST, instance=mascota)
        form_observacion = AgregarObservacionForm(request.POST)

        if 'guardar_mascota' in request.POST:
            if form_mascota.is_valid():
                form_mascota.save()
                return redirect('ficha_mascota', mascota_id=mascota_id)

        if 'agregar_observacion' in request.POST:
            if form_observacion.is_valid():
                nueva_observacion = form_observacion.save(commit=False)
                nueva_observacion.mascota = mascota
                # Asignar el médico que realiza la observación
                nueva_observacion.medico = request.user.medico
                nueva_observacion.save()
                return redirect('ficha_mascota', mascota_id=mascota_id)
    else:
        form_mascota = EditarMascotaForm(instance=mascota)
        form_observacion = AgregarObservacionForm()

    return render(request, 'ficha_mascota.html', {
        'mascota': mascota,
        'observaciones': observaciones,
        'form_mascota': form_mascota,
        'form_observacion': form_observacion,
    })

# Vista para ver el detalle de una observación específica


def detalle_observacion_view(request, observacion_id):
    observacion = get_object_or_404(Observacion, id=observacion_id)
    return render(request, 'detalle_observacion.html', {'observacion': observacion})

# Vista para el chat de los veterinarios


def chat_view(request):
    cliente = request.session.get('cliente', None)
    if not cliente:
        return redirect('login')

    conversaciones = Conversacion.objects.filter(participantes=cliente['id'])
    return render(request, 'chat.html', {'conversaciones': conversaciones})

# Vistas para el control de citas


def control_citas_view(request):
    citas = Cita.objects.all()
    return render(request, 'control_citas.html', {'citas': citas})


def agregar_cita_view(request):
    if request.method == 'POST':
        form = SolicitarCitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('control_citas')
    else:
        form = SolicitarCitaForm()

    return render(request, 'agregar_cita.html', {'form': form})


def editar_cita_view(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)

    if request.method == 'POST':
        form = SolicitarCitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            return redirect('control_citas')
    else:
        form = SolicitarCitaForm(instance=cita)

    return render(request, 'editar_cita.html', {'form': form})


def eliminar_cita_view(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)

    if request.method == 'POST':
        cita.delete()
        return redirect('control_citas')

    return render(request, 'eliminar_cita.html', {'cita': cita})

# Vista para agregar un registro médico


def agregar_registro_medico_view(request):
    if request.method == 'POST':
        form = RegistroMedicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_registros_medicos')
    else:
        form = RegistroMedicoForm()
    return render(request, 'agregar_registro_medico.html', {'form': form})

# Vista para ver la lista de registros médicos


def lista_registros_medicos_view(request):
    registros = RegistroMedico.objects.all()
    return render(request, 'lista_registros_medicos.html', {'registros': registros})

# Vista para manejar el inicio de sesión


def login(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        password = request.POST.get('password')
        try:
            cliente = Cliente.objects.get(correo=correo)
            if check_password(password, cliente.password):
                request.session['cliente'] = {
                    'id': cliente.id,
                    'nombre': cliente.nombre,
                    'correo': cliente.correo,
                }
                return redirect('interfaz')
            else:
                return render(request, 'index.html', {'error': 'Contraseña incorrecta.'})
        except Cliente.DoesNotExist:
            return render(request, 'index.html', {'error': 'Usuario no encontrado.'})
    return render(request, 'index.html')

# Vista para subir una foto (aún no implementada)


def upload_photo(request):
    return render(request, 'upload_photo.html')

# Vista para cerrar sesión


def logout_view(request):
    auth_logout(request)
    # Redirigir al index.html para que el usuario pueda volver a iniciar sesión
    return redirect('index')
