from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.models import ShippingAddress, Order, OrderItem
from payment.forms import ShippingForm, PaymentForm
from django.contrib import messages
from django.contrib.auth.models import User
from ecom.models import Product, Profile

def payment_success(request):
    return render(request, "payment/payment_success.html", {})

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form })
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})
    
def billing_info(request):
	if request.POST:
		cart = Cart(request)
		cart_products = cart.get_prods
		quantities = cart.get_quants
		totals = cart.cart_total()

		my_shipping = request.POST
		request.session['my_shipping'] = my_shipping

		if request.user.is_authenticated:
			billing_form = PaymentForm()
			return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})

		else:
			billing_form = PaymentForm()
			return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})

	else:
		messages.success(request, "Access Denied")
		return redirect('home')

def process_order(request):
	if request.POST:
		cart = Cart(request)
		cart_products = cart.get_prods
		quantities = cart.get_quants
		totals = cart.cart_total()

		payment_form = PaymentForm(request.POST or None)
		my_shipping = request.session.get('my_shipping')

		full_name = my_shipping['shipping_full_name']
		email = my_shipping['shipping_email']

		shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
		amount_paid = totals

		if request.user.is_authenticated:
			user = request.user
			create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
			create_order.save()

			order_id = create_order.pk
			
			for product in cart_products():
				product_id = product.id
				if product.is_sale:
					price = product.sale_price
				else:
					price = product.price

				for key,value in quantities().items():
					if int(key) == product.id:
						create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
						create_order_item.save()
			
			for key in list(request.session.keys()):
				if key == "session_key":
					del request.session[key]

			current_user = Profile.objects.filter(user__id=request.user.id)
			current_user.update(old_cart="")
	
			return redirect('payment_success')
		
		else:
			create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
			create_order.save()
			order_id = create_order.pk
			
			for product in cart_products():
				product_id = product.id
				if product.is_sale:
					price = product.sale_price
				else:
					price = product.price

				for key,value in quantities().items():
					if int(key) == product.id:
						create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
						create_order_item.save()
			
			for key in list(request.session.keys()):
				if key == "session_key":
					del request.session[key]

			return redirect('payment_success')

	else:
		return redirect('home')
