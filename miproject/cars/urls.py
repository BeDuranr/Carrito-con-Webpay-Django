from itertools import product
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from .views import SignUpView

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'),name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('eliminar_producto/<str:nombre_producto>/', views.eliminar_producto, name='eliminar_producto'),
    path('obtener-clima/', views.obtener_clima, name='obtener_clima'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)