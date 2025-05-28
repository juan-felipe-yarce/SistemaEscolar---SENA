# core/views/docente_hoja_vida.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from core.models import HojaDeVidaDocente
from core.forms import (
    DatosBasicosDocenteForm,
    IdentificacionForm,
    IdentidadForm
)

@login_required
def docente_datos_basicos_view(request):
    usuario = request.user
    perfil = getattr(usuario, 'perfil', None)

    try:
        hoja_de_vida = HojaDeVidaDocente.objects.get(usuario=usuario)
    except HojaDeVidaDocente.DoesNotExist:
        hoja_de_vida = None

    if request.method == 'POST':
        form_identificacion = IdentificacionForm(request.POST, instance=usuario)
        form_identidad = IdentidadForm(request.POST, instance=perfil)
        form_basico = DatosBasicosDocenteForm(request.POST, instance=hoja_de_vida)

        # ⚠️ Validación personalizada para el campo adicional
        if all([form_identificacion.is_valid(), form_identidad.is_valid(), form_basico.is_valid()]):
            usuario = form_identificacion.save(commit=False)
            municipio_ident = form_identificacion.cleaned_data.get('municipio_identificacion')

            usuario.save()
            
            if perfil:
                perfil.municipio_identificacion = municipio_ident
                perfil.save()
            
            form_identidad.save()

            hoja = form_basico.save(commit=False)
            hoja.usuario = usuario
            hoja.save()

            messages.success(request, "✅ Información actualizada correctamente.")
            return redirect('docente_datos_basicos')
        else:
            print("Errores Identificación:", form_identificacion.errors)
            print("Errores Identidad:", form_identidad.errors)
            print("Errores Básico:", form_basico.errors)
            messages.error(request, "❌ Corrige los errores en los formularios.")
    else:
        form_identificacion = IdentificacionForm(instance=usuario)
        form_identidad = IdentidadForm(instance=perfil)
        form_basico = DatosBasicosDocenteForm(instance=hoja_de_vida)

    context = {
        'form_identificacion': form_identificacion,
        'form_identidad': form_identidad,
        'form_basico': form_basico,
        'hoja': hoja_de_vida
    }
    return render(request, 'panel_docente/datos_basicos.html', context)
