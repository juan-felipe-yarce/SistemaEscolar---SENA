from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from core.models import (
    NivelEducativo, Grado, Aula, Grupo,
    Asignatura, Area, Tema, Logro,
    AsignacionDocente
)
from core.forms import (
    NivelEducativoForm, GradoForm, AulaForm, GrupoForm,
    AsignacionDocenteForm, AreaForm, AsignaturaForm,
    TemaForm, LogroForm
)

def es_coordinador(user):
    return user.rol.nombre == 'Coordinador Académico'

# Y a continuación, todas las funciones tal como están en tu views.py:
# lista_niveles, crear_nivel, editar_nivel, eliminar_nivel, etc...
# Módulos del Coordinador Académico
# Niveles
@login_required
@user_passes_test(es_coordinador)
def lista_niveles(request):
    niveles = NivelEducativo.objects.all()
    return render(request, 'panel_coordinador/nivel_list.html', {'niveles': niveles})

@login_required
@user_passes_test(es_coordinador)
def crear_nivel(request):
    form = NivelEducativoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Nivel Educativo creado correctamente.")
        return redirect('lista_niveles')
    return render(request, 'panel_coordinador/nivel_form.html', {'form': form})

@login_required
@user_passes_test(es_coordinador)
def editar_nivel(request, pk):
    nivel = NivelEducativo.objects.get(pk=pk)
    form = NivelEducativoForm(request.POST or None, instance=nivel)
    if form.is_valid():
        form.save()
        messages.success(request, "Nivel Educativo actualizado.")
        return redirect('lista_niveles')
    return render(request, 'panel_coordinador/nivel_form.html', {'form': form})

@login_required
@user_passes_test(es_coordinador)
def eliminar_nivel(request, pk):
    NivelEducativo.objects.get(pk=pk).delete()
    messages.success(request, "Nivel Educativo eliminado.")
    return redirect('lista_niveles')

# Grados
@login_required
@user_passes_test(es_coordinador)
def lista_grados(request):
    grados = Grado.objects.all()
    return render(request, 'panel_coordinador/grado_list.html', {'grados': grados})

@login_required
@user_passes_test(es_coordinador)
def crear_grado(request):
    form = GradoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Grado creado correctamente.")
        return redirect('lista_grados')
    return render(request, 'panel_coordinador/grado_form.html', {'form': form})

@login_required
@user_passes_test(es_coordinador)
def editar_grado(request, pk):
    grado = Grado.objects.get(pk=pk)
    form = GradoForm(request.POST or None, instance=grado)
    if form.is_valid():
        form.save()
        messages.success(request, "Grado actualizado correctamente.")
        return redirect('lista_grados')
    return render(request, 'panel_coordinador/grado_form.html', {'form': form})

@login_required
@user_passes_test(es_coordinador)
def eliminar_grado(request, pk):
    Grado.objects.get(pk=pk).delete()
    messages.success(request, "Grado eliminado correctamente.")
    return redirect('lista_grados')

# Areas
@login_required
@user_passes_test(es_coordinador)
def lista_areas(request):
    areas = Area.objects.all()
    return render(request, 'panel_coordinador/area_list.html', {'areas': areas})

@login_required
@user_passes_test(es_coordinador)
def crear_area(request):
    form = AreaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Área creada correctamente.")
        return redirect('lista_areas')
    return render(request, 'panel_coordinador/area_form.html', {'form': form})

@login_required
@user_passes_test(es_coordinador)
def editar_area(request, pk):
    area = Area.objects.get(pk=pk)
    form = AreaForm(request.POST or None, instance=area)
    if form.is_valid():
        form.save()
        messages.success(request, "Área actualizada correctamente.")
        return redirect('lista_areas')
    return render(request, 'panel_coordinador/area_form.html', {'form': form})

@login_required
@user_passes_test(es_coordinador)
def eliminar_area(request, pk):
    Area.objects.get(pk=pk).delete()
    messages.success(request, "Área eliminada correctamente.")
    return redirect('lista_areas')

# Asignaturas
@login_required
@user_passes_test(es_coordinador)
def lista_asignaturas(request):
    asignaturas = Asignatura.objects.all()
    return render(request, 'panel_coordinador/asignatura_list.html', {'asignaturas': asignaturas})

@login_required
@user_passes_test(es_coordinador)
def crear_asignatura(request):
    form = AsignaturaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Asignatura creada correctamente.")
        return redirect('lista_asignaturas')
    return render(request, 'panel_coordinador/asignatura_form.html', {'form': form})

@login_required
@user_passes_test(es_coordinador)
def editar_asignatura(request, pk):
    asignatura = Asignatura.objects.get(pk=pk)
    form = AsignaturaForm(request.POST or None, instance=asignatura)
    if form.is_valid():
        form.save()
        messages.success(request, "Asignatura actualizada correctamente.")
        return redirect('lista_asignaturas')
    return render(request, 'panel_coordinador/asignatura_form.html', {'form': form})

@login_required
@user_passes_test(es_coordinador)
def eliminar_asignatura(request, pk):
    Asignatura.objects.get(pk=pk).delete()
    messages.success(request, "Asignatura eliminada correctamente.")
    return redirect('lista_asignaturas')

# Temas
@login_required
@user_passes_test(es_coordinador)
def lista_temas(request):
    temas = Tema.objects.all()
    return render(request, 'panel_coordinador/tema_list.html', {'temas': temas})

@login_required
@user_passes_test(es_coordinador)
def crear_tema(request):
    form = TemaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Tema creado correctamente.")
        return redirect('lista_temas')
    return render(request, 'panel_coordinador/tema_form.html', {'form': form})

@login_required
@user_passes_test(es_coordinador)
def editar_tema(request, pk):
    tema = Tema.objects.get(pk=pk)
    form = TemaForm(request.POST or None, instance=tema)
    if form.is_valid():
        form.save()
        messages.success(request, "Tema actualizado correctamente.")
        return redirect('lista_temas')
    return render(request, 'panel_coordinador/tema_form.html', {'form': form})

@login_required
@user_passes_test(es_coordinador)
def eliminar_tema(request, pk):
    Tema.objects.get(pk=pk).delete()
    messages.success(request, "Tema eliminado correctamente.")
    return redirect('lista_temas')

# Logros
@login_required
@user_passes_test(es_coordinador)
def lista_logros(request):
    logros = Logro.objects.all()
    return render(request, 'panel_coordinador/logro_list.html', {'logros': logros})

@login_required
@user_passes_test(es_coordinador)
def crear_logro(request):
    form = LogroForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Logro creado correctamente.")
        return redirect('lista_logros')
    return render(request, 'panel_coordinador/logro_form.html', {'form': form})

@login_required
@user_passes_test(es_coordinador)
def editar_logro(request, pk):
    logro = Logro.objects.get(pk=pk)
    form = LogroForm(request.POST or None, instance=logro)
    if form.is_valid():
        form.save()
        messages.success(request, "Logro actualizado correctamente.")
        return redirect('lista_logros')
    return render(request, 'panel_coordinador/logro_form.html', {'form': form})

@login_required
@user_passes_test(es_coordinador)
def eliminar_logro(request, pk):
    Logro.objects.get(pk=pk).delete()
    messages.success(request, "Logro eliminado correctamente.")
    return redirect('lista_logros')

# Aulas
@login_required
@user_passes_test(es_coordinador)
def lista_aulas(request):
    aulas = Aula.objects.all()
    return render(request, 'panel_coordinador/aula_list.html', {'aulas': aulas})

@login_required
@user_passes_test(es_coordinador)
def crear_aula(request):
    form = AulaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Aula creada correctamente.")
        return redirect('lista_aulas')
    return render(request, 'panel_coordinador/aula_form.html', {'form': form})

@login_required
@user_passes_test(es_coordinador)
def editar_aula(request, pk):
    aula = Aula.objects.get(pk=pk)
    form = AulaForm(request.POST or None, instance=aula)
    if form.is_valid():
        form.save()
        messages.success(request, "Aula actualizada correctamente.")
        return redirect('lista_aulas')
    return render(request, 'panel_coordinador/aula_form.html', {'form': form})

@login_required
@user_passes_test(es_coordinador)
def eliminar_aula(request, pk):
    Aula.objects.get(pk=pk).delete()
    messages.success(request, "Aula eliminada correctamente.")
    return redirect('lista_aulas')

# Grupos
@login_required
@user_passes_test(es_coordinador)
def lista_grupos(request):
    grupos = Grupo.objects.all()
    return render(request, 'panel_coordinador/grupo_list.html', {'grupos': grupos})

@login_required
@user_passes_test(es_coordinador)
def crear_grupo(request):
    form = GrupoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Grupo creado correctamente.")
        return redirect('lista_grupos')
    return render(request, 'panel_coordinador/grupo_form.html', {'form': form})

@login_required
@user_passes_test(es_coordinador)
def editar_grupo(request, pk):
    grupo = Grupo.objects.get(pk=pk)
    form = GrupoForm(request.POST or None, instance=grupo)
    if form.is_valid():
        form.save()
        messages.success(request, "Grupo actualizado correctamente.")
        return redirect('lista_grupos')
    return render(request, 'panel_coordinador/grupo_form.html', {'form': form})

@login_required
@user_passes_test(es_coordinador)
def eliminar_grupo(request, pk):
    Grupo.objects.get(pk=pk).delete()
    messages.success(request, "Grupo eliminado correctamente.")
    return redirect('lista_grupos')

# Asignación Docente
@login_required
@user_passes_test(es_coordinador)
def lista_asignaciones(request):
    asignaciones = AsignacionDocente.objects.all()
    return render(request, 'panel_coordinador/asignacion_docente_list.html', {'asignaciones': asignaciones})

@login_required
@user_passes_test(es_coordinador)
def crear_asignacion(request):
    form = AsignacionDocenteForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Asignación creada correctamente.")
        return redirect('lista_asignaciones')
    return render(request, 'panel_coordinador/asignacion_docente_form.html', {'form': form})

@login_required
@user_passes_test(es_coordinador)
def editar_asignacion(request, pk):
    asignacion = AsignacionDocente.objects.get(pk=pk)
    form = AsignacionDocenteForm(request.POST or None, instance=asignacion)
    if form.is_valid():
        form.save()
        messages.success(request, "Asignación actualizada correctamente.")
        return redirect('lista_asignaciones')
    return render(request, 'panel_coordinador/asignacion_docente_form.html', {'form': form})

@login_required
@user_passes_test(es_coordinador)
def eliminar_asignacion(request, pk):
    AsignacionDocente.objects.get(pk=pk).delete()
    messages.success(request, "Asignación eliminada correctamente.")
    return redirect('lista_asignaciones')