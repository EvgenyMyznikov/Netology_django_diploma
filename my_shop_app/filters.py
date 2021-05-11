from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from my_shop_app.models import Product, Order, Review


class ProductFilter(filters.FilterSet):
    max_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    description = filters.CharFilter(field_name='description', lookup_expr='contains')

    class Meta:
        model = Product
        fields = ('name', 'description', 'max_price', 'min_price')


class ReviewFilter(filters.FilterSet):
    author_id = filters.ModelChoiceFilter(field_name='author_id', to_field_name='id', queryset=User.objects.all())
    product_id = filters.ModelChoiceFilter(field_name='product_id', to_field_name='id', queryset=Product.objects.all())
    created_at = filters.DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = Review
        fields = ('author_id', 'product_id', 'created_at')


class OrderFilter(filters.FilterSet):
    STATUSES = (
        ('1', 'NEW'),
        ('2', 'IN_PROGRESS'),
        ('3', 'DONE')
    )
    id = filters.ModelMultipleChoiceFilter(to_field_name="id", queryset=Order.objects.all())
    status = filters.ChoiceFilter(choices=STATUSES, field_name='order_status')
    amount_from = filters.NumberFilter(field_name='order_price', lookup_expr='gte')
    amount_to = filters.NumberFilter(field_name='order_price', lookup_expr='lte')
    created_at = filters.DateFromToRangeFilter(field_name='created_at')
    updated_at = filters.DateFromToRangeFilter(field_name='updated_at')
    positions = filters.ModelChoiceFilter(field_name="products", to_field_name="id", queryset=Product.objects.all())

    class Meta:
        model = Order
        fields = ("id", 'status', "amount_from", "amount_to", 'created_at', 'updated_at', 'positions')
