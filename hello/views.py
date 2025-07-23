from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def hello_world(request):
    """
    Vista que renderiza el template HTML con archivos estáticos
    """
    return render(request, 'hello/index.html')
