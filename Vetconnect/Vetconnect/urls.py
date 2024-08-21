"""
URL configuration for Vetconnect project.

The `urlpatterns` list routes URLs to views. For more information, please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from mi_app import views
from mi_app.views import agregar_registro_medico_view, lista_registros_medicos_view


urlpatterns = [
    # Ruta para la administración del sitio
    path('admin/', admin.site.urls),

    # Ruta para la página principal
    path('', views.index, name='index'),

    # Ruta para la página de creación de usuarios (registro)
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),

    # Ruta para la comprobación de los datos de registro
    path('comprobacion/', views.ingresar_usuario, name='ingresar_usuario'),

    # Ruta para la página de inicio de sesión
    path('login/', views.login, name='login'),

    # Ruta para la interfaz principal después del inicio de sesión
    path('interfaz/', views.interfaz, name='interfaz'),

    # Ruta para ver el perfil del usuario
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),

    # Ruta para editar el perfil del usuario
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),

    # Rutas para ingresar y gestionar mascotas
    path('ingresar_mascota/', views.ingresar_mascota_view,
         name='ingresar_mascota'),  # Ruta para ingresar una nueva mascota
    # Ruta para guardar una nueva mascota o actualizar una existente
    path('guardar_mascota/', views.guardar_mascota, name='guardar_mascota'),
    path('guardar_mascota/<int:mascota_id>/', views.guardar_mascota,
         name='guardar_mascota'),  # Ruta para actualizar una mascota existente
    path('eliminar_mascota/<int:mascota_id>/', views.eliminar_mascota_view,
         name='eliminar_mascota'),  # Ruta para eliminar una mascota
    path('editar_mascota/<int:mascota_id>/', views.editar_mascota_view,
         name='editar_mascota'),  # Ruta para editar mascota

    # Rutas para gestionar citas
    path('solicitar_cita/', views.solicitar_cita_view,
         name='solicitar_cita'),  # Ruta para solicitar una nueva cita
    path('proximas_citas/', views.proximas_citas_view,
         name='proximas_citas'),  # Ruta para ver las próximas citas
    # Ruta para Guardar la nueva cita
    path('guardar_cita/', views.guardar_cita_view, name='guardar_cita'),
    # Control de citas
    path('control_citas/', views.control_citas_view, name='control_citas'),
    path('control_citas/agregar/', views.agregar_cita_view, name='agregar_cita'),
    path('control_citas/editar/<int:cita_id>/',
         views.editar_cita_view, name='editar_cita'),
    path('control_citas/eliminar/<int:cita_id>/',
         views.eliminar_cita_view, name='eliminar_cita'),
    # ruta de los REgistros medicos :
    path('ficha_mascota/<int:mascota_id>/',
         views.ficha_mascota_view, name='ficha_mascota'),
    path('agregar_registro_medico/', agregar_registro_medico_view,
         name='agregar_registro_medico'),
    path('lista_registros_medicos/', lista_registros_medicos_view,
         name='lista_registros_medicos'),

    # Ruta para ver la lista de mascotas
    path('ver_mascotas/', views.ver_mascotas_view, name='ver_mascotas'),

    # Ruta para la página de chat
    path('chat/', views.chat_view, name='chat'),

    # Ruta para subir una foto
    path('upload-photo/', views.upload_photo, name='upload_photo'),

    # Ruta para cerrar sesión
    path('logout/', views.logout_view, name='logout'),
]
