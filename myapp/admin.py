from django.contrib import admin
from .models import Product, Category, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'created_at', 'ordered_products']
    inlines = [OrderItemInline]

    def ordered_products(self, obj):
        print(f"DEBUG: Обробка замовлення ID: {obj.id}")  # Відладковий print
        items = obj.items.all()
        print(f"DEBUG: Знайдено OrderItems для замовлення {obj.id}: {list(items)}")  # Відладковий print

        if not items:
            print(f"DEBUG: Не знайдено товарів для замовлення {obj.id}")  # Відладковий print
            return "– (Немає товарів)"  # Повертаємо маркер, якщо товарів немає

        product_list = []
        for item in items:
            product_name = "N/A"
            if hasattr(item, 'product') and item.product:  # Додаткова перевірка
                product_name = item.product.name
            else:
                print(f"DEBUG: У OrderItem ID {item.id} відсутній товар (product).")

            product_list.append(f"{product_name} x{item.quantity}")

        result = ", ".join(product_list)
        print(f"DEBUG: Сформований список для замовлення {obj.id}: '{result}'")  # Відладковий print
        return result

    ordered_products.short_description = "Список товарів"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'available']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']