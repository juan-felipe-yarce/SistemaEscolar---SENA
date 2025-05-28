from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def panel_docente_view(request):
    return render(request, 'panel_docente/dashboard_base.html')
