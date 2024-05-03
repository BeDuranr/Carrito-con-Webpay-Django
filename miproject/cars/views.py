from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Product, Cart, CartItem, Order, OrderItem
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@login_required
def add_to_cart(request, product_id):
    # Obtener el producto
    product = get_object_or_404(Product, pk=product_id)
    # Obtener o crear el carrito para el usuario actual
    cart, created = Cart.objects.get_or_create(user=request.user)
    # Obtener o crear el item del carrito para el producto
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    # Incrementar la cantidad del producto en el carrito
    cart_item.quantity += 1
    cart_item.save()
    # Redirigir a la lista de productos
    return redirect('product_list')

def view_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitem_set.all()
    return render(request, 'cart.html', {'cart_items': cart_items})

def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(pk=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')

def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitem_set.all()
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    order = Order.objects.create(user=request.user, total_amount=total_amount)
    for cart_item in cart_items:
        OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity, unit_price=cart_item.product.price)
    cart.delete()
    return redirect('order_success')
