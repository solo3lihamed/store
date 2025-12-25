from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from products.models import Product
from django.views.decorators.http import require_POST

def cart_add(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1
    request.session['cart'] = cart
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
    return redirect('cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        total_price += product.price * quantity
        cart_items.append({'product': product, 'quantity': quantity, 'total_price': product.price * quantity})
    
    return render(request, 'orders/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def order_create(request):
    cart = request.session.get('cart', {})
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        
        user = request.user if request.user.is_authenticated else None
        
        order = Order.objects.create(full_name=full_name, address=address, phone_number=phone_number, user=user)
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, pk=product_id)
            OrderItem.objects.create(order=order, product=product, price=product.price, quantity=quantity)
        
        # Clear cart
        request.session['cart'] = {}
        return render(request, 'orders/created.html', {'order': order})
    
    # Calculate total for display
    total_price = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        total_price += product.price * quantity

    return render(request, 'orders/create.html', {'total_price': total_price})
