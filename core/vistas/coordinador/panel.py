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
        'pendientes': usuarios,  # <--- este nombre debe coincidir con el de la plantilla
        'pending_users_count': usuarios.count()
    })


@login_required
@user_passes_test(es_coordinador)
def activar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    # Validación: solo permitir activar usuarios con rol Docente
    if usuario.rol.nombre != 'Docente':
        messages.error(request, "❌ Solo se pueden activar cuentas de tipo Docente.")
        return redirect('usuarios_pendientes')

    # Verificación: evitar reactivación innecesaria
    if usuario.is_active:
        messages.warning(request, f"⚠️ El usuario {usuario.correo} ya está activo.")
    else:
        usuario.is_active = True
        usuario.save()
        messages.success(request, f"✅ Usuario {usuario.correo} activado correctamente.")

    return redirect('usuarios_pendientes')
