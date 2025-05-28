from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def docente_capacitacion_view(request):
    return render(request, 'panel_docente/capacitacion.html')  # crea esta plantilla también
