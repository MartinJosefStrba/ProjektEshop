from django.shortcuts import render
from .models import Product

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def rozvoj(request):
    products = Product.objects.filter(category__name="Osobní rozvoj")
    return render(request, 'osobniRozvoj.html', {'products': products})

def poezie(request):
    products = Product.objects.filter(category__name="Poezie a drama")
    return render(request, 'poeziedrama.html', {'products': products})

def mladez(request):
    products = Product.objects.filter(category__name="Pro děti a mládež")
    return render(request, 'detimladez.html', {'products': products})

def naucna(request):
    products = Product.objects.filter(category__name="Naučná")
    return render(request, 'naucna.html', {'products': products})

def beletrie(request):
    products = Product.objects.filter(category__name="Beletrie")
    return render(request, 'beletrie.html', {'products': products})
