from django.contrib import admin
from my_shop_app.models import Product, Review, ProductOrderPosition, Order, ProductCollection, Collection


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'name', 'description', 'created_at', 'updated_at')
    list_display_links = ('name',)
    list_filter = ('price', 'name', 'description')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_id', 'product_id', 'text', 'created_at')
    list_display_links = ('author_id', 'product_id', 'text')
    list_filter = ('author_id', 'product_id', 'created_at')


class ProductOrderPositionInLine(admin.TabularInline):
    model = ProductOrderPosition


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'order_price', 'order_status', 'created_at', 'updated_at']
    list_filter = ['buyer', 'created_at', 'updated_at']
    inlines = [ProductOrderPositionInLine]


class ProductCollectionInLine(admin.TabularInline):
    model = ProductCollection


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'created_at', 'updated_at')
    list_display_links = ('id', 'title')
    inlines = [ProductCollectionInLine]


admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Order, OrderAdmin)
