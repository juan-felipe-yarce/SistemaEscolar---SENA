from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def panel_docente_view(request):
    return redirect('docente_datos_basicos')
