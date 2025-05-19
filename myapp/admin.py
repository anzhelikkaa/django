# shopeasy/admin.py

from django.contrib import admin
from .models import Category, Product
from django.contrib import admin
from .models import Order

admin.site.register(Order)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available', 'brand', 'warranty_years', 'created_at')
    list_filter = ('available', 'category', 'brand')
    search_fields = ('name', 'description', 'brand')
