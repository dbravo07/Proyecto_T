from django.db import models

# Modelo para representar a los médicos veterinarios


class MedicoVeterinario(models.Model):
    nombre = models.CharField(max_length=255)
    especialidad = models.CharField(max_length=255)
    correo = models.EmailField(max_length=255)
    telefono = models.CharField(max_length=20)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


# Modelo para representar a los clientes
class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    rut = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(max_length=255, unique=True)
    direccion = models.CharField(max_length=255)
    creado = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


# Modelo para representar las mascotas de los clientes
class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=100)
    raza = models.CharField(max_length=100)
    sexo = models.CharField(max_length=10)
    edad = models.IntegerField()
    peso = models.FloatField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    # Otros campos relevantes

    def __str__(self):
        return self.nombre


# Modelo para representar las observaciones de los medicos
class Observacion(models.Model):
    mascota = models.ForeignKey(
        Mascota, on_delete=models.CASCADE, related_name='observaciones')
    medico = models.ForeignKey(MedicoVeterinario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    nota = models.TextField()

    def __str__(self):
        return f"Observación de {self.medico} en {self.mascota.nombre} - {self.fecha}"


# Modelo para representar los veterinarios (este es el nuevo modelo Veterinario)
class Veterinario(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del veterinario
    # Especialidad del veterinario
    especialidad = models.CharField(max_length=100)
    # Indica si está disponible para consultas
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - {self.especialidad}"


# Modelo para representar las citas veterinarias
class Cita(models.Model):
    AREA_CHOICES = [
        ('Control', 'Control'),
        ('Consulta', 'Consulta'),
        ('Procedimiento', 'Procedimiento'),
    ]

    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, default=1)
    especialidad = models.CharField(max_length=100)
    area = models.CharField(max_length=20, choices=AREA_CHOICES)
    medico = models.ForeignKey(Veterinario, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField()
    hora_seleccionada = models.BooleanField(default=False)

    def __str__(self):
        return f"Cita para {self.cliente.nombre} con {self.medico.nombre} en {self.fecha} a las {self.hora}"

    class Meta:
        permissions = [
            ("can_view_own_data", "Can view own data"),
            ("can_add_pet", "Can add pet"),
            ("can_view_pet", "Can view pet"),
            ("can_edit_pet", "Can edit pet"),
            ("can_delete_pet", "Can delete pet"),
            ("can_request_appointment", "Can request appointment"),
            ("can_manage_appointments", "Can manage appointments"),
            ("can_view_appointments", "Can view appointments"),
            ("can_view_chat", "Can view chat"),
            ("can_manage_chat", "Can manage chat"),
        ]


# Modelo para representar las conversaciones entre veterinarios
class Conversacion(models.Model):
    participantes = models.ManyToManyField(MedicoVeterinario)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Conversación {self.id}'


# Modelo para representar los mensajes en una conversación
class MensajeConversacion(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE)
    autor = models.ForeignKey(
        MedicoVeterinario, on_delete=models.CASCADE)  # Autor del mensaje
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    def __str__(self):
        return f'Mensaje de {self.autor.nombre} en conversación {self.conversacion.id}'


# Modelo para Registros médicos
class RegistroMedico(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    medico = models.ForeignKey(MedicoVeterinario, on_delete=models.CASCADE)
    fecha = models.DateField()
    descripcion = models.TextField()

    def __str__(self):
        return f"Registro de {self.mascota.nombre} - {self.fecha}"
