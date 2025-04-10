from django.contrib import admin
from django.contrib.auth.models import User
from .models import Category, Customer, Product, Order, Profile, Subscriber

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'author',)
    search_fields = ('name', 'author',)
    ordering = ('name',)   

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(Profile)

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscribed')
    search_fields = ('email',)

admin.site.register(Subscriber, SubscriberAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

