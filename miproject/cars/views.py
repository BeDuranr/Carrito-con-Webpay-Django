from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import requests
from .models import Product, Cart, CartItem, Order, OrderItem
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from transbank.webpay.webpay_plus.transaction import Transaction





class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
     cart_item.quantity += 1
     cart_item.save()
    return redirect('product_list')

def view_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitem_set.all()
    return render(request, 'cart.html', {'cart_items': cart_items})

def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(pk=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')


def agregar_producto(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        product = Product.objects.create(name=name, description=description, price=price, image=image,)
        return redirect('product_list')
    return render(request, 'agregar_producto.html')

def eliminar_producto(request, nombre_producto):
    try:
        producto = Product.objects.get(name=nombre_producto)
        producto.delete()
    except Product.DoesNotExist:
        pass
    return redirect('product_list')



def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitem_set.all()
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    order = Order.objects.create(user=request.user, total_amount=total_amount)
    for cart_item in cart_items:
        OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity, unit_price=cart_item.product.price)
    transbank = Transaction.configure_for_testing()
    transaction_instance = Transaction()
    response = transaction_instance.create(buy_order='1', session_id='user', amount=total_amount, return_url='https://callback/resultado/de/transaccion')
    return redirect(response['url']) 

def obtener_clima(request):
    ciudad = request.GET.get('ciudad', 'Santiago')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={settings.OPENWEATHERMAP_API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()

    # Formatear los datos del clima en HTML
    clima_html = f'<strong>Ciudad:</strong> {data["name"]}<br>'
    clima_html += f'<strong>Temperatura:</strong> {data["main"]["temp"]}°C<br>'

    return JsonResponse({'html': clima_html})



