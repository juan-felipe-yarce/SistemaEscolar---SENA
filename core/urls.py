from django.conf import settings
from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
from .views import (
    inicio, login_usuario, registro_usuario, perfil_usuario,
    panel_coordinador, panel_docente, panel_estudiante, panel_acudiente,
    usuarios_pendientes, activar_usuario,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('bienvenida/', views.bienvenida, name='bienvenida'),

    # Página de inicio
    path('', views.inicio, name='inicio'),  # Esto maneja http://127.0.0.1:8000/
    
    # Cerrar
    path('logout/', views.logout_usuario, name='logout'),

    # Registro de usuarios
    path('registro/', views.registro_usuario, name='registro'),

    # Login de usuarios
    path('login/', views.login_usuario, name='login'),
    
    # Perfil del usuario autenticado
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),


    # Paneles de usuario (Coordinador, Docente, Estudiante, Acudiente)
    path('panel-docente/', views.panel_docente, name='panel_docente'),
    path('panel-estudiante/', views.panel_estudiante, name='panel_estudiante'),
    path('panel-coordinador/', views.panel_coordinador, name='panel_coordinador'),
    path('panel-acudiente/', views.panel_acudiente, name='panel_acudiente'),

    # Rutas para la gestión del currículo y áreas educativas por el Coordinador Académico
    # Niveles Educativos
    path('coordinador/niveles/', views.lista_niveles, name='lista_niveles'),
    path('coordinador/niveles/nuevo/', views.crear_nivel, name='crear_nivel'),
    path('coordinador/niveles/editar/<int:pk>/', views.editar_nivel, name='editar_nivel'),
    path('coordinador/niveles/eliminar/<int:pk>/', views.eliminar_nivel, name='eliminar_nivel'),

    # Grados
    path('coordinador/grados/', views.lista_grados, name='lista_grados'),
    path('coordinador/grados/nuevo/', views.crear_grado, name='crear_grado'),
    path('coordinador/grados/editar/<int:pk>/', views.editar_grado, name='editar_grado'),
    path('coordinador/grados/eliminar/<int:pk>/', views.eliminar_grado, name='eliminar_grado'),
    
    # Aulas
    path('coordinador/aulas/', views.lista_aulas, name='lista_aulas'),
    path('coordinador/aulas/nuevo/', views.crear_aula, name='crear_aula'),
    path('coordinador/aulas/editar/<int:pk>/', views.editar_aula, name='editar_aula'),
    path('coordinador/aulas/eliminar/<int:pk>/', views.eliminar_aula, name='eliminar_aula'),

    # Grupos
    path('coordinador/grupos/', views.lista_grupos, name='lista_grupos'),
    path('coordinador/grupos/nuevo/', views.crear_grupo, name='crear_grupo'),
    path('coordinador/grupos/editar/<int:pk>/', views.editar_grupo, name='editar_grupo'),
    path('coordinador/grupos/eliminar/<int:pk>/', views.eliminar_grupo, name='eliminar_grupo'),

    # Asignaciones Docentes
    path('coordinador/asignaciones/', views.lista_asignaciones, name='lista_asignaciones'),
    path('coordinador/asignaciones/nuevo/', views.crear_asignacion, name='crear_asignacion'),
    path('coordinador/asignaciones/editar/<int:pk>/', views.editar_asignacion, name='editar_asignacion'),
    path('coordinador/asignaciones/eliminar/<int:pk>/', views.eliminar_asignacion, name='eliminar_asignacion'),

    # Coordinador Usuarios Pendientes
    path('coordinador/usuarios-pendientes/', usuarios_pendientes, name='usuarios_pendientes'),
    path('coordinador/activar-usuario/<int:usuario_id>/', activar_usuario, name='activar_usuario'),

    
    # Áreas
    path('coordinador/areas/', views.lista_areas, name='lista_areas'),
    path('coordinador/areas/nuevo/', views.crear_area, name='crear_area'),
    path('coordinador/areas/editar/<int:pk>/', views.editar_area, name='editar_area'),
    path('coordinador/areas/eliminar/<int:pk>/', views.eliminar_area, name='eliminar_area'),

    # Asignaturas
    path('coordinador/asignaturas/', views.lista_asignaturas, name='lista_asignaturas'),
    path('coordinador/asignaturas/nuevo/', views.crear_asignatura, name='crear_asignatura'),
    path('coordinador/asignaturas/editar/<int:pk>/', views.editar_asignatura, name='editar_asignatura'),
    path('coordinador/asignaturas/eliminar/<int:pk>/', views.eliminar_asignatura, name='eliminar_asignatura'),

    # Temas
    path('coordinador/temas/', views.lista_temas, name='lista_temas'),
    path('coordinador/temas/nuevo/', views.crear_tema, name='crear_tema'),
    path('coordinador/temas/editar/<int:pk>/', views.editar_tema, name='editar_tema'),
    path('coordinador/temas/eliminar/<int:pk>/', views.eliminar_tema, name='eliminar_tema'),

    # Logros
    path('coordinador/logros/', views.lista_logros, name='lista_logros'),
    path('coordinador/logros/nuevo/', views.crear_logro, name='crear_logro'),
    path('coordinador/logros/editar/<int:pk>/', views.editar_logro, name='editar_logro'),
    path('coordinador/logros/eliminar/<int:pk>/', views.eliminar_logro, name='eliminar_logro'),
]

# Solo en modo desarrollo
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]


