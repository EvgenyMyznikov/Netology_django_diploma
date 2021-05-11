from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from my_shop_app.models import User, Product, Review, Order, Collection
from rest_framework.viewsets import ModelViewSet
from my_shop_app.serializers import ProductSerializer, ReviewSerializer, OrderSerializer, CollectionSerializer, \
    UserSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from my_shop_app.permissions import IsAuthorOrReadOnly
from my_shop_app.filters import ProductFilter, ReviewFilter, OrderFilter


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user)

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action in ["create", ]:
            permission_classes = [IsAuthenticated]
        elif self.action in ["update", "destroy"]:
            permission_classes = [IsAuthorOrReadOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

    def get_permissions(self):
        if self.action in ["create", "list"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.prefetch_related('positions').all()
        if self.request.user.is_authenticated:
            return Order.objects.prefetch_related('positions').filter(buyer=self.request.user.id)
        else:
            raise ValidationError("Для работы с заказом необходимо авторизоваться!")


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    filter_backends = [DjangoFilterBackend]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
