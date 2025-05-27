from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('checkout/', views.checkout, name='checkout'),  # БЕЗ <pk>
    path('cart/', views.cart_view, name='cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('order-success/', views.order_success, name='order_success'),
    path('ajax/update-cart/', views.update_cart_ajax, name='update_cart_ajax'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
