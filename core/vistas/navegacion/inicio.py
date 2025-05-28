# Inicio, autenticación y redirección por rol
from django.shortcuts import render, redirect

def bienvenida(request):
    return render(request, 'inicio.html')

def inicio(request):
    if request.user.is_authenticated:
        rol = request.user.rol.nombre
        redirecciones = {
            'Coordinador Académico': 'panel_coordinador',
            'Docente': 'panel_docente',
            'Estudiante': 'panel_estudiante',
            'Acudiente': 'panel_acudiente',
            'Padre de Familia o Acudiente': 'panel_acudiente',
        }
        return redirect(redirecciones.get(rol, 'login'))
    return redirect('login')
