# Importaciones y utilidades
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import (
    Usuario, NivelEducativo, Grado, Area, Asignatura, Tema, Logro,
    PerfilDeUsuario, Aula, Grupo, AsignacionDocente
)
from .forms import (
    LoginForm, RegistroUsuarioForm, PerfilUsuarioForm,
    NivelEducativoForm, GradoForm, AreaForm, AsignaturaForm,
    TemaForm, LogroForm, AulaForm, GrupoForm, AsignacionDocenteForm
)

def es_coordinador(user):
    return user.rol.nombre == 'Coordinador Académico'

# Inicio, autenticación y redirección por rol
def bienvenida(request):
    return render(request, 'inicio.html')

def inicio(request):
    if not request.session.get('inicio_visitado'):
        request.session['inicio_visitado'] = True
        if request.user.is_authenticated:
            logout(request)
    if request.user.is_authenticated:
        return redirect('panel_coordinador')
    return render(request, 'inicio.html')

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Usuario registrado correctamente. Ya puedes iniciar sesión.")
            return redirect('login')
        else:
            messages.error(request, "❌ Verifica los errores en el formulario.")
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})

def login_usuario(request):
    error = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            password = form.cleaned_data['password']
            try:
                usuario = Usuario.objects.get(correo=correo)
                if usuario.check_password(password):
                    login(request, usuario)
                    redirecciones = {
                        'Coordinador Académico': 'panel_coordinador',
                        'Docente': 'panel_docente',
                        'Estudiante': 'panel_estudiante',
                        'Acudiente': 'panel_acudiente',
                        'Padre de Familia o Acudiente': 'panel_acudiente',
                    }
                    destino = redirecciones.get(usuario.rol.nombre)
                    return redirect(reverse(destino)) if destino else HttpResponse("Rol no reconocido.")
                else:
                    error = "Contraseña incorrecta"
            except Usuario.DoesNotExist:
                error = "Usuario no encontrado"
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'error': error})

# Paneles por rol
@login_required
def perfil_usuario(request):
    usuario = request.user
    perfil = getattr(usuario, 'perfil', None)  # Evita errores si no existe

    return render(request, 'core/perfil_usuario.html', {
        'usuario': usuario,
        'perfil': perfil
    })



@login_required
def editar_perfil(request):
    try:
        perfil = request.user.perfil
    except PerfilDeUsuario.DoesNotExist:
        perfil = PerfilDeUsuario(usuario=request.user)
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
    return render(request, 'core/editar_perfil.html', {'form': form})

def panel_docente(request):
    return HttpResponse("Panel del Docente")

def panel_estudiante(request):
    return HttpResponse("Panel del Estudiante")

def panel_acudiente(request):
    return HttpResponse("Panel del Acudiente")

@login_required
@user_passes_test(es_coordinador)
def panel_coordinador(request):
    return render(request, 'panel_coordinador/panel_coordinador.html')

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

