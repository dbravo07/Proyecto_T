from django import forms
from .models import Cita, Veterinario, Mascota, RegistroMedico, Observacion


# Definición del formulario para solicitar una cita

class SolicitarCitaForm(forms.ModelForm):
    class Meta:
        # Especifica el modelo que se utilizará para crear este formulario
        model = Cita
        # Define los campos del formulario que serán mostrados y gestionados en el formulario
        fields = ['medico', 'mascota', 'area', 'fecha', 'hora', 'motivo']
        # Personaliza los widgets para los campos del formulario
        widgets = {
            # 'fecha' se presentará como un input de tipo 'date', lo que permitirá al usuario seleccionar una fecha a través de un calendario
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            # 'hora' será un input oculto; el valor de la hora seleccionada se establecerá mediante JavaScript al seleccionar una hora en el frontend
            'hora': forms.HiddenInput(),  # Oculta el campo de hora
        }

    def __init__(self, *args, **kwargs):
        cliente_id = kwargs.pop('cliente_id', None)
        super(SolicitarCitaForm, self).__init__(*args, **kwargs)
        if cliente_id:
            self.fields['mascota'].queryset = Mascota.objects.filter(
                cliente_id=cliente_id)


class RegistroMedicoForm(forms.ModelForm):
    class Meta:
        model = RegistroMedico
        fields = ['mascota', 'medico', 'fecha', 'descripcion']


class EditarMascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'sexo', 'edad', 'peso']


class AgregarObservacionForm(forms.ModelForm):
    class Meta:
        model = Observacion
        fields = ['nota']
