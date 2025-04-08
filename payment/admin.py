from django.contrib import admin
from django.contrib.auth.models import User
from .models import ShippingAddress, Order, OrderItem
from django.utils import timezone

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    fields = (("user", "full_name"), "email", "shipping_address", "amount_paid", "date_ordered", "shipped", "date_shipped")
    list_display = ('id', 'email', 'amount_paid', 'shipped', 'date_ordered', 'days_since_creation')
    list_filter = ('date_ordered',)
    inlines = [OrderItemInline]
    actions = ('set_orders_to_shipped', )

    def set_orders_to_shipped(self, request, queryset):
        count = queryset.update(shipped=True)
        self.message_user(request, '{} objednávky označeny jako odeslány'.format(count))
    set_orders_to_shipped.short_description = 'Označit objednávky jako odeslané'

    def days_since_creation(self, order):
        diff = timezone.now() - order.date_ordered
        return diff.days

admin.site.register(ShippingAddress)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
