from django.contrib import admin
from .models import User, Category, Listing, Watchlist, Purchase

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_active')
    list_filter = ('is_active', 'date_joined')
    search_fields = ('username', 'email')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'price', 'quantity', 'quantity_sold', 'quantity_available', 'category', 'isActive', 'isSold', 'created_at')
    list_filter = ('isActive', 'isSold', 'category', 'created_at')
    search_fields = ('title', 'description', 'owner__username')
    readonly_fields = ('created_at', 'sold_at', 'quantity_sold')
    
    def quantity_available(self, obj):
        return obj.quantity_available()
    quantity_available.short_description = 'Available'

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('listing', 'buyer', 'seller', 'quantity_purchased', 'purchase_price', 'total_price', 'purchase_date')
    list_filter = ('purchase_date', 'listing__category')
    search_fields = ('listing__title', 'buyer__username', 'seller__username')
    readonly_fields = ('purchase_date',)

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'created_at')
    list_filter = ('created_at', 'listing__category')
    search_fields = ('user__username', 'listing__title')
    readonly_fields = ('created_at',)