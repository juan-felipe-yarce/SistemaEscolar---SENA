from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Usuario, Rol, TipoDocumento, Pais, Departamento, Ciudad,
    Genero, EstadoCivil, Estrato,
    NivelEducativo, Grado, Area, Asignatura,
    Tema, Logro, Aula,
    PerfilDeUsuario, AsignacionDocente, Grupo
)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('correo', 'rol', 'is_active', 'activado_por_display', 'fecha_creacion', 'es_superusuario')
    list_filter = ('is_active', 'rol__nombre')
    search_fields = ('correo', 'numero_documento')
    ordering = ('-fecha_creacion',)
    actions = ['activar_usuarios_seleccionados']

    def activado_por_display(self, obj):
        return obj.activado_por.correo if obj.activado_por else "—"
    activado_por_display.short_description = "Activado por"

    def es_superusuario(self, obj):
        return obj.is_superuser
    es_superusuario.boolean = True
    es_superusuario.short_description = "Superuser"

    @admin.action(description="Activar usuarios seleccionados")
    def activar_usuarios_seleccionados(self, request, queryset):
        activados = 0
        for usuario in queryset:
            if not usuario.is_active:
                usuario.is_active = True
                usuario.activado_por = request.user
                usuario.save()
                activados += 1
        self.message_user(request, f"✅ Se activaron {activados} usuario(s).")

# Registra Rol también (si no lo tienes aún)
@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    
admin.site.register(TipoDocumento)
admin.site.register(Pais)
admin.site.register(Departamento)
admin.site.register(Ciudad)
admin.site.register(Genero)
admin.site.register(EstadoCivil)
admin.site.register(Estrato)
admin.site.register(PerfilDeUsuario)
admin.site.register(AsignacionDocente)
admin.site.register(Grupo)
admin.site.register(Aula)
admin.site.register(NivelEducativo)
admin.site.register(Grado)
admin.site.register(Area)
admin.site.register(Asignatura)
admin.site.register(Tema)
admin.site.register(Logro)
