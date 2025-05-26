# core/context_processors.py

from core.models import Usuario

def pending_users_count(request):
    if request.user.is_authenticated and hasattr(request.user, 'rol') and request.user.rol.nombre == "Coordinador Académico":
        count = Usuario.objects.filter(is_active=False).exclude(rol__nombre="Coordinador Académico").count()
        return {'pending_users_count': count}
    return {}

