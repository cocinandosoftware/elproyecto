from django.shortcuts import render
from django.http import HttpResponse

from web.models import Ciudad

# Create your views here.

def index(request):


    nombre: str = "Sergi de CocinandoSoftware 99"

    ciudades = Ciudad.objects.all()

    return render(request, 'web/index.html', {'nombre': nombre, 'ciudades': ciudades})