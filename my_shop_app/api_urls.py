from rest_framework.routers import DefaultRouter
from my_shop_app.views import ProductViewSet, ReviewViewSet, OrderViewSet, CollectionViewSet, UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename='users')
router.register("products", ProductViewSet, basename="products")
router.register("product-reviews", ReviewViewSet, basename="reviews")
router.register("orders", OrderViewSet, basename="orders")
router.register("product-collections", CollectionViewSet, basename="collections")

urlpatterns = router.urls
