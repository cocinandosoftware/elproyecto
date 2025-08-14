from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):
    return render(request, 'web/index.html')

def test_index(request):
    return render(request, 'web/test_index.html')

def test_main(request):
    return render(request, 'web/test_main.html')