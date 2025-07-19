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
    return redirect('lista_niveles')

@login_required
@user_passes_test(es_coordinador)
def usuarios_pendientes(request):
    # Mostrar solo usuarios inactivos que NO sean Coordinadores
    usuarios = Usuario.objects.filter(
        is_active=False
    ).exclude(
        rol__nombre__iexact='Coordinador Académico'
    ).select_related('rol')

    return render(request, 'panel_coordinador/usuarios_pendientes.html', {
        'pendientes': usuarios,
        'pending_users_count': usuarios.count()
    })


@login_required
@user_passes_test(es_coordinador)
def activar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    # ⚠️ Si el usuario que va a activar es Coordinador Académico...
    if usuario.rol.nombre == 'Coordinador Académico':
        messages.error(request, "❌ No tienes permisos para activar a otros Coordinadores Académicos. Solo el Superusuario puede hacerlo.")
        return redirect('usuarios_pendientes')

    # ⚠️ Evitar activación duplicada
    if usuario.is_active:
        messages.warning(request, f"⚠️ El usuario {usuario.correo} ya está activo.")
    else:
        usuario.is_active = True
        usuario.activado_por = request.user  # ✅ Registro de quién activó
        usuario.save()
        messages.success(request, f"✅ Usuario {usuario.correo} activado correctamente.")

    return redirect('usuarios_pendientes')
