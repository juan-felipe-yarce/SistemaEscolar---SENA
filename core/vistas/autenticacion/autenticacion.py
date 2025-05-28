from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms

from core.forms import RegistroUsuarioForm, PerfilUsuarioForm, LoginForm
from core.models import PerfilDeUsuario, Rol, Usuario



def login_usuario(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('inicio')
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
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
            form.save()
            messages.success(request, "Registro exitoso.")
            return redirect('login')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'registro.html', {'form': form})
