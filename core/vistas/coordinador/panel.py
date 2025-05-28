from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from core.models import Usuario
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

def es_coordinador(user):
    return user.rol.nombre == 'Coordinador Académico'

@login_required
@user_passes_test(es_coordinador)
def panel_coordinador(request):
    return redirect('usuarios_pendientes')

@login_required
@user_passes_test(es_coordinador)
def usuarios_pendientes(request):
    usuarios = Usuario.objects.filter(is_active=False)
    return render(request, 'panel_coordinador/usuarios_pendientes.html', {
        'usuarios': usuarios,
        'pending_users_count': usuarios.count()
    })

@login_required
@user_passes_test(es_coordinador)
def activar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.is_active = True
    usuario.save()
    messages.success(request, f"✅ Usuario {usuario.correo} activado correctamente.")
    return redirect('usuarios_pendientes')
