from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # create or get session cart
    cart = request.session.get('cart', {})

    # add or increase quantity
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')

def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity
        })

    total = sum(item['total_price'] for item in cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

def buy(request):
    cart = request.session.get('cart', {})

    if not cart:
        return HttpResponse("Your cart is empty.")

    try:
        with transaction.atomic():
            for product_id, quantity in cart.items():
                product = get_object_or_404(Product, id=product_id)

                if product.quantity < quantity:
                    return HttpResponse(f"Not enough stock for {product.name}.")

                product.quantity -= quantity
                product.save()

            # clear the cart after successful purchase
            request.session['cart'] = {}
            request.session.modified = True

        return HttpResponse("Purchase successful!")

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}")


