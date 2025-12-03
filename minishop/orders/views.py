from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from cart.models import Cart
from orders.models import *
from .forms import *
from cart.views import remove_from_cart
from django.views.generic import ListView, DeleteView
from orders.order_creator import *
from orders.delivery_calculator import *


def order_create(request):
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Создаем объект Order, но не сохраняем его в базу данных сразу
            order = form.save(commit=False)
            # Присваиваем текущего пользователя
            order.user = request.user
            # Сохраняем объект в базу данных
            order.save()

            # Добавляем товары из корзины в заказ
            cart_items = Cart.objects.filter(user=request.user)
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.total_price,
                    quantity=item.quantity
                )
            # Очищаем корзину
            cart_items.delete()
            return redirect('main')
    else:
        form = OrderCreateForm()
    return render(request, 'order_create.html', {'form': form})


def orders_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders_list.html', {'orders': orders})


class Order_detail(ListView):

    model = Order
    template_name = 'order_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        order_items = VendorOrder.objects.select_related(
            'vendor',
            'parent_order'
        ).prefetch_related(
            'items',
            'items__product'
        ).filter(parent_order_id=self.kwargs['id'])

        #context['total_price'] = sum([i.get_cost() for i in order_items.items.all()])
        #context['total_count'] = sum([i.quantity for i in order_items.items.all()])
        context['order_items'] = order_items
        return context


def clear_cart(request):
    """
    Очищает корзину пользователя
    """
    try:
        cart = Cart.objects.filter(user=request.user)
        # В зависимости от вашей модели корзины, либо удаляем все товары, либо очищаем поле
        cart.items.all().delete()  # если у вас связь через ForeignKey/ManyToMany
        #cart.cart_items.all().delete()
        cart.save()
        return True
    except Cart.DoesNotExist:
        return False


class Delete_order(LoginRequiredMixin, DeleteView):

    model = Order
    success_url = reverse_lazy('orders_list')

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект заказа
        order = self.get_object()

        # Проверка прав доступа
        if order.user != request.user and not request.user.is_staff:
            raise PermissionDenied("У вас нет прав для редактирования этого товара")

        return super().dispatch(request, *args, **kwargs)


def checkout(request):
    try:
        cart = Cart.objects.filter(user=request.user)
        if not cart:
            return False
    except Cart.DoesNotExist:
        return False

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            user_data = {
                'user': request.user,
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'address': form.cleaned_data['address'],
                'postal_code': form.cleaned_data['postal_code'],
                'city': form.cleaned_data['city'],
            }

            order = OrderCreator.create_order_from_cart(cart, user_data)
            cart_items = Cart.objects.filter(user=request.user)
            cart_items.delete()
            #remove_from_cart()  # Очищаем корзину

            return redirect('orders_list')

    else:
        form = OrderForm()

    # Предварительный расчет доставки для отображения
    delivery_preview = {}
    vendor_totals = {}

    # Группируем товары по продавцам для предварительного расчета
    vendor_items = {}
    for item in cart:
        vendor = item.product.vendor
        if vendor not in vendor_items:
            vendor_items[vendor] = []
        vendor_items[vendor].append(item)

    # Рассчитываем стоимость для каждого продавца
    for vendor, items in vendor_items.items():
        items_total = sum(item.product.discounted_price * item.quantity for item in items)
        vendor_totals[vendor] = items_total

        # Если город выбран, рассчитываем доставку
        if request.GET.get('city'):
            delivery_cost = DeliveryCalculator.calculate_delivery_cost(
                vendor, request.GET.get('city'), items_total
            )
            delivery_preview[vendor] = {
                'delivery_cost': delivery_cost,
                'total': items_total + delivery_cost
            }

    return render(request, 'checkout.html', {
        'form': form,
        'vendor_totals': vendor_totals,
        'delivery_preview': delivery_preview,
        'cart': cart,
        'vendor_items': vendor_items
    })


def order_confirmation(request, order_id):
    order = Order.objects.prefetch_related('vendor_orders__items').get(id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})