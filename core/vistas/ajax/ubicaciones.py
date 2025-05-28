from django.http import JsonResponse
from core.models import Departamento, Ciudad


def obtener_departamentos(request):
    pais_id = request.GET.get('pais_id')

    if pais_id:
        departamentos = Departamento.objects.filter(pais_id=pais_id).values('id', 'nombre').order_by('nombre')
        return JsonResponse(list(departamentos), safe=False)
    else:
        return JsonResponse([], safe=False)


def obtener_ciudades(request):
    departamento_id = request.GET.get('departamento_id')

    if departamento_id:
        ciudades = Ciudad.objects.filter(departamento_id=departamento_id).values('id', 'nombre').order_by('nombre')
        return JsonResponse(list(ciudades), safe=False)
    else:
        return JsonResponse([], safe=False)
