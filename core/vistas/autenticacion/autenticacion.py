from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from core.forms import RegistroUsuarioForm, PerfilUsuarioForm, LoginForm
from core.models import PerfilDeUsuario, Rol, Usuario


def login_usuario(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data["usuario"]
            login(request, usuario)

            # Redirección según el rol
            nombre_rol = usuario.rol.nombre.lower()
            if nombre_rol == "coordinador académico":
                return redirect('panel_coordinador')
            elif nombre_rol == "docente":
                return redirect('panel_docente')
            elif nombre_rol == "estudiante":
                return redirect('panel_estudiante')
            elif nombre_rol in ["acudiente", "padre de familia o acudiente"]:
                return redirect('panel_acudiente')
            else:
                return redirect('inicio')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_usuario(request):
    logout(request)
    return redirect('bienvenida')


def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.is_superuser = False
            usuario.is_staff = False
            usuario.is_active = False  # La cuenta debe ser activada posteriormente
            usuario.save()
            messages.success(request, "✅ Registro exitoso. Tu cuenta ha sido creada y será activada por el personal autorizado.")
            return redirect('login')
        else:
            messages.error(request, "❌ Corrige los errores del formulario.")
    else:
        form = RegistroUsuarioForm()

    return render(request, 'registro.html', {'form': form})
