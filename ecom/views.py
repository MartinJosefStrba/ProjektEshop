from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
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

def product(request, pk):
     product = Product.objects.get(id=pk)
     return render(request, 'product.html', {'product':product})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
    
    else:
        return render(request, 'login.html', {})
    
def logout_user(request):
    logout(request)
    return redirect('home')

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('update_info')
		else:
			return redirect('register')
	else:
		return render(request, 'register.html', {'form':form})