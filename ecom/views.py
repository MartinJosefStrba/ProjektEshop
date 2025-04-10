from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm, SubscriberForm
from django import forms
from .models import Product, Profile
from django.contrib import messages
from django.db.models import Q
import json
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress

def subscribe_view(request):
    if request.method == 'POST':
          form = SubscriberForm(request.POST)
          if form.is_valid():
               form.save()
               messages.success(request, 'Děkujem za příhlášení k odběru')
               return redirect('subscribe')
          else:
               messages.success(request, 'Tento mail je již přihlášen k odběru')
               return redirect('subscribe')
    else:
         form = SubscriberForm()
    return render(request, 'subscribe.html', {'form':form})

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

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']

        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched) | Q(author__icontains=searched))

        if not searched:
            return render(request, "search.html", {})
        else:
             return render(request, "search.html", {'searched':searched})
    else:
         return render(request, "search.html", {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart

            if saved_cart:
                 converted_cart = json.loads(saved_cart)
                 cart = Cart(request)

                 for key, value in converted_cart.items():
                      cart.db_add(product=key, quantity=value)

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
     
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            return redirect('home')
          
        return render(request, "update_user.html", {'user_form':user_form})

    else:
         return redirect('home') 
    
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')  
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form':form})
    else:
        return redirect('home')
    
def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()

            return redirect('home')
        
        return render(request, "update_info.html", {'form': form, 'shipping_form': shipping_form})
    else:
        return redirect('home')