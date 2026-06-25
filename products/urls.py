from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),

    # CART ROUTES
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('buy/', views.buy, name='buy'),

#     path('new', views.new),
]
