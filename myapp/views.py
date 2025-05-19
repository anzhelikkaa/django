from .models import Product, Category, Order
from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrderForm

def index(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()
    selected_category = None

    if category_id:
        selected_category = get_object_or_404(Category, pk=category_id)
        products = Product.objects.filter(category=selected_category)
    else:
        products = Product.objects.all()

    return render(request, 'index.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category
    })
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = category.products.all()
    return render(request, 'category_detail.html', {'category': category, 'products': products})
def add_to_cart(request, pk):
    cart = request.session.get('cart', [])
    if pk not in cart:
        cart.append(pk)
        request.session['cart'] = cart
    return redirect('cart')

def remove_from_cart(request, pk):
    cart = request.session.get('cart', [])
    if pk in cart:
        cart.remove(pk)
        request.session['cart'] = cart
    return redirect('cart')

def cart_view(request):
    cart_ids = request.session.get('cart', [])
    products = Product.objects.filter(pk__in=cart_ids)
    total = sum([p.price for p in products])
    return render(request, 'cart.html', {'products': products, 'total': total})
def checkout(request):
    cart_ids = request.session.get('cart', [])
    products = Product.objects.filter(pk__in=cart_ids)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            for product in products:
                order = form.save(commit=False)
                order.product = product
                order.save()
            request.session['cart'] = []  # Очистити кошик
            return render(request, 'order_success.html', {'order': order})
    else:
        form = OrderForm()

    return render(request, 'checkout.html', {'form': form, 'products': products})
