from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from my_shop_app.models import User, Product, Review, Order, ProductOrderPosition, ProductCollection, Collection


class UserSerializer(serializers.ModelSerializer):
    review_author = serializers.PrimaryKeyRelatedField(many=True, queryset=Review.objects.all())
    order = serializers.PrimaryKeyRelatedField(many=True, queryset=Order.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'review_author', 'order',)


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для Product."""
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)

    class Meta:
        model = Product
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для Review."""
    author_id = serializers.ReadOnlyField(source='author_id.username')
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Review
        fields = ('id', 'author_id', 'product_id', 'rating',
                  'text', 'created_at', 'updated_at',)

    def create(self, validated_data):
        validated_data['author_id'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        current_user = self.context['request'].user
        product = self.context['request'].data['product_id']
        method = self.context['request'].stream.method
        reviews = Review.objects.filter(product_id=product).filter(author_id=current_user).count()
        if reviews and method == 'POST':
            raise ValidationError({'error': 'Вы можете оставить только 1 отзыв на данный товар!'})
        return data


class ProductOrderPositionSerializer(serializers.ModelSerializer):
    """Сериализатор для ProductOrderPosition."""

    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True, )
    quantity = serializers.IntegerField(min_value=1, default=1, )

    class Meta:
        model = ProductOrderPosition
        fields = ('id', 'product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для Order."""

    order = serializers.ReadOnlyField(source='order.username')
    positions = ProductOrderPositionSerializer(many=True)
    order_price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0, max_value=1000000, default=0)

    class Meta:
        model = Order
        fields = ('id', 'buyer', 'order', 'positions', 'order_price', 'order_status')
        read_only_fields = ('buyer', 'order_price')

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        order = super().create(validated_data)
        order_price = 0
        if positions:
            to_save = []
            for item in positions:
                order_price += item['product'].price * item['quantity']
                to_save.append(ProductOrderPosition.objects.create(
                    product=item['product'],
                    quantity=item['quantity'],
                    order_id=order.id,
                ))
        order.order_price = order_price
        order.save()
        return order


class ProductCollectionSerializer(serializers.ModelSerializer):
    """Сериализатор для ProductCollection."""
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True, )
    name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = ProductCollection
        fields = ('product_id', 'name')


class CollectionSerializer(serializers.ModelSerializer):
    """Сериализатор для Collection."""
    collections = ProductCollectionSerializer(many=True)
    title = serializers.CharField(required=True, )
    text = serializers.CharField(required=False, )

    class Meta:
        model = Collection
        fields = ('id', 'title', 'text', 'collections', 'created_at', 'updated_at',)

    def create(self, validated_data):
        collections_data = validated_data.pop('collections')
        collection = super().create(validated_data)
        for elem in collections_data:
            ProductCollection.objects.create(
                product=elem['product_id'],
                collection=collection,
            )
        return collection
