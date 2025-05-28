from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import PerfilUsuarioForm
from core.models import PerfilDeUsuario

@login_required
def perfil_usuario(request):
    usuario = request.user
    perfil = getattr(usuario, 'perfil', None)
     # Detecta el rol para asignar el dashboard base correcto
    if request.user.rol.nombre == 'Coordinador Académico':
        base_template = 'panel_coordinador/dashboard_base.html'
    elif request.user.rol.nombre == 'Docente':
        base_template = 'panel_docente/dashboard_base.html'
    else:
        base_template = 'base.html'

    return render(request, 'perfil_usuario.html', {
        'usuario': usuario,
        'perfil': perfil,
        'base_template': base_template,  # 👈 se pasa al template
    })

@login_required
def editar_perfil(request):
    try:
        perfil = request.user.perfil
    except PerfilDeUsuario.DoesNotExist:
        perfil = PerfilDeUsuario(usuario=request.user)

    # ⚠️ Agrega esta lógica para definir la plantilla base
    if request.user.rol.nombre == 'Coordinador Académico':
        base_template = 'panel_coordinador/dashboard_base.html'
    elif request.user.rol.nombre == 'Docente':
        base_template = 'panel_docente/dashboard_base.html'
    else:
        base_template = 'base.html'

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, request.FILES, instance=perfil, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Perfil actualizado correctamente.')
            return redirect('editar_perfil')
        else:
            messages.error(request, '❌ Corrige los errores del formulario.')
    else:
        form = PerfilUsuarioForm(instance=perfil, user=request.user)

    return render(request, 'editar_perfil.html', {
        'form': form,
        'base_template': base_template,  # 👈 Esto es clave
    })
