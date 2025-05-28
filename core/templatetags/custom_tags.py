from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def obtener_dashboard_base(context):
    usuario = context['request'].user
    if hasattr(usuario, 'rol'):
        nombre_rol = usuario.rol.nombre.lower()
        if nombre_rol == 'docente':
            return 'panel_docente/dashboard_base.html'
        elif nombre_rol == 'coordinador':
            return 'panel_coordinador/dashboard_base.html'
    return 'base.html'