# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category
from django.contrib import messages
from .forms import OrderForm
from .models import Product, OrderItem
from django.http import JsonResponse
import json

def index(request):
    categories = Category.objects.all()
    selected_category = None
    products = Product.objects.filter(available=True)

    category_id = request.GET.get('category')
    if category_id:
        selected_category = get_object_or_404(Category, pk=category_id)
        products = products.filter(category=selected_category)

    return render(request, 'index.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    is_available = product.stock > 0
    return render(request, 'product_detail.html', {
        'product': product,
        'is_available': is_available
    })


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk, available=True)
    cart = request.session.get('cart', {})

    if str(pk) in cart:
        new_qty = cart[str(pk)] + 1
        if new_qty <= product.stock:
            cart[str(pk)] = new_qty
        else:
            messages.warning(request, f"Максимальна кількість для '{product.name}' — {product.stock}.")
    else:
        cart[str(pk)] = 1

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    allow_checkout = True

    for pid, quantity in cart.items():
        product = get_object_or_404(Product, pk=pid)
        subtotal = product.price * quantity
        available = product.stock >= quantity
        if not available:
            allow_checkout = False

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
            'available': available,
        })
        total += subtotal

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'allow_checkout': allow_checkout,
    })

def update_cart(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        for key in request.POST:
            if key.startswith('quantity_'):
                pid = key.split('_')[1]
                product = get_object_or_404(Product, pk=pid)
                try:
                    quantity = int(request.POST[key])
                    if quantity <= 0:
                        cart.pop(pid, None)
                    elif quantity <= product.stock:
                        cart[pid] = quantity
                    else:
                        messages.warning(request, f"Максимальна кількість для '{product.name}' — {product.stock}.")
                except ValueError:
                    messages.error(request, "Невірне значення кількості.")

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart')

def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        del cart[str(pk)]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart')

from django import forms

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)

def checkout(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0
    adjusted_cart = {}
    has_out_of_stock = False

    for pk, quantity in cart.items():
        try:
            product = Product.objects.get(pk=pk)
            if product.stock == 0:
                messages.error(request, f"Товар '{product.name}' немає в наявності.")
                has_out_of_stock = True
                continue
            elif quantity > product.stock:
                messages.warning(request, f"Товар '{product.name}' має лише {product.stock} шт. — кількість змінено.")
                adjusted_cart[str(pk)] = product.stock
                quantity = product.stock
            else:
                adjusted_cart[str(pk)] = quantity

            products.append({'product': product, 'quantity': quantity})
            total += product.price * quantity

        except Product.DoesNotExist:
            messages.error(request, f"Товар з ID {pk} не знайдено.")
            has_out_of_stock = True

    if adjusted_cart != cart:
        request.session['cart'] = adjusted_cart
        request.session.modified = True
        return redirect('checkout')

    if has_out_of_stock:
        return redirect('cart')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in products:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity']
                )
                # 🔥 Update stock after purchase
                item['product'].stock -= item['quantity']
                item['product'].save()

            request.session['cart'] = {}
            return render(request, 'order_success.html', {'order': order})
    else:
        form = OrderForm()

    return render(request, 'checkout.html', {
        'cart_items': products,
        'total': total,
        'form': form
    })

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = category.products.filter(available=True)
    return render(request, 'category_detail.html', {
        'category': category,
        'products': products
    })

def order_success(request):
    return render(request, 'order_success.html')

def update_cart_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pid = str(data.get('product_id'))
            quantity = int(data.get('quantity'))

            cart = request.session.get('cart', {})

            if quantity > 0:
                cart[pid] = quantity
            else:
                cart.pop(pid, None)

            request.session['cart'] = cart
            request.session.modified = True
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request'})
