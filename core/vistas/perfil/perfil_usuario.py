from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import PerfilUsuarioForm
from core.models import PerfilDeUsuario

@login_required
def perfil_usuario(request):
    usuario = request.user
    try:
        perfil = usuario.perfil
    except PerfilDeUsuario.DoesNotExist:
        perfil = None

    # Detecta el rol para asignar el dashboard base correcto
    if usuario.rol and usuario.rol.nombre == 'Coordinador Académico':
        base_template = 'panel_coordinador/dashboard_base.html'
    elif usuario.rol and usuario.rol.nombre == 'Docente':
        base_template = 'panel_docente/dashboard_base.html'
    else:
        base_template = 'base.html'

    return render(request, 'perfil_usuario.html', {
        'usuario': usuario,
        'perfil': perfil,
        'base_template': base_template,
    })


@login_required
def editar_perfil(request):
    usuario = request.user
    try:
        perfil = usuario.perfil
    except PerfilDeUsuario.DoesNotExist:
        perfil = None

    # Detecta el rol para el template base
    if usuario.rol and usuario.rol.nombre == 'Coordinador Académico':
        base_template = 'panel_coordinador/dashboard_base.html'
    elif usuario.rol and usuario.rol.nombre == 'Docente':
        base_template = 'panel_docente/dashboard_base.html'
    else:
        base_template = 'base.html'

    # --- CORREGIDO: Limpieza de mensajes duplicados o rezagados ---
    # Limpia mensajes solo si es GET y vienes de un redirect (opcional avanzado)
    # from django.contrib.messages import get_messages
    # list(get_messages(request))

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, request.FILES, instance=perfil, user=usuario)
        if form.is_valid():
            perfil_nuevo = form.save(commit=False)
            perfil_nuevo.usuario = usuario

            # Asegura que la ciudad esté presente (por modelo o por lógica extra)
            if not perfil_nuevo.ciudad:
                form.add_error('ciudad', "La ciudad de residencia es obligatoria.")
                return render(request, 'editar_perfil.html', {
                    'form': form,
                    'base_template': base_template,
                })

            perfil_nuevo.save()
            form.save_m2m()
            messages.success(request, '✅ Perfil actualizado correctamente.')
            return redirect('editar_perfil')  # Good practice: POST-Redirect-GET
        else:
            messages.error(request, '❌ Corrige los errores del formulario.')
    else:
        form = PerfilUsuarioForm(instance=perfil, user=usuario)

    return render(request, 'editar_perfil.html', {
        'form': form,
        'base_template': base_template,
    })
