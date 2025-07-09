from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def bienvenida(request):
    return render(request, 'inicio.html')  # plantilla pública sin login


@login_required
def inicio(request):
    user = request.user

    if user.is_superuser:
        # 🔐 Si es superusuario, redirigir directamente al admin
        return redirect('/admin/')

    if user.rol is None:
        messages.error(request, "Tu cuenta no tiene un rol asignado. Contacta al administrador.")
        return redirect('logout')

    rol = user.rol.nombre
    redirecciones = {
        'Coordinador Académico': 'panel_coordinador',
        'Docente': 'panel_docente',
        'Estudiante': 'panel_estudiante',
        'Acudiente': 'panel_acudiente',
        'Padre de Familia o Acudiente': 'panel_acudiente',
    }

    return redirect(redirecciones.get(rol, 'login'))
