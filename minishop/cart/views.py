from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import Cart
from magazine.models import *


@login_required
def add_to_cart(request, product_id):
    cart_item = Cart.objects.filter(user=request.user, product_id=product_id).first()
    product = Product.objects.get(id=product_id)
    if cart_item:
        cart_item.quantity += 1
        cart_item.total_price += product.discounted_price
        cart_item.save()
    else:
        Cart.objects.create(user=request.user, product_id=product.id, price=product.discounted_price, total_price=product.discounted_price, product_name=product.product_name)
    return JsonResponse({'success': True, 'message': 'Товар добавлен в корзину!', 'cart_count': Cart.objects.filter(user=request.user).count()})


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id)
    if cart_item.user == request.user:
        cart_item.delete()
    return redirect("cart")


@login_required
def cart_detail(request):
    images = {}
    cart_items = Cart.objects.filter(user=request.user)
    cart_items_counts = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total']
    cart_items_total_price = Cart.objects.filter(user=request.user).aggregate(total=Sum('total_price'))['total']
    product_id_list = [i.product_id for i in cart_items]
    for i in product_id_list:
        images[i] = ["".join(u) for u in Product_image.objects.filter(product=i).values_list('image')]
    context = {
        "cart_items": cart_items,
        'cart_items_counts': cart_items_counts,
        'cart_items_total_price': cart_items_total_price,
        "product_id_list": product_id_list,
        "images": images,
    }
    return render(request, "cart.html", context)


@login_required
def update_cart_item(request, product_id, action):
    cart_item = Cart.objects.filter(user=request.user, product_id=product_id).first()
    product = Product.objects.get(id=product_id)

    if action == 'increase':
        cart_item.quantity += 1
        cart_item.total_price += product.discounted_price
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.total_price -= product.discounted_price

    cart_item.save()

    return redirect('cart')