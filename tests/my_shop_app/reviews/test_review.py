import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, \
    HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from tests.my_shop_app.reviews.conftest import review_factory, product_factory
from tests.my_shop_app.test_product import test_create_product_admin
from my_shop_app.models import Review


# список отзывов
@pytest.mark.django_db
def test_list_reviews(unauthorized_client):
    url = reverse('reviews-list')
    resp = unauthorized_client.get(url)
    assert resp.status_code == HTTP_200_OK


# создание отзыва неавторизованным пользователем
@pytest.mark.django_db
def test_create_review_unauthorized(unauthorized_client, admin_client):
    url = reverse('reviews-list')
    product = test_create_product_admin(admin_client)
    review = {
        "product_id": product["id"],
        "rating": 5,
        "text": "Стильный товар"
    }
    resp = unauthorized_client.post(url, review, format='json')
    assert resp.status_code == HTTP_401_UNAUTHORIZED
    assert Review.objects.count() == 0


# создание отзыва авторизованным пользователем
@pytest.mark.django_db
def test_update_or_delete_own_review(api_client, product_factory):
    url = reverse('reviews-list')
    product = product_factory()
    review = {
        'product_id': product.id,
        'rating': 5,
        'text': "Стильный товар",
    }
    resp = api_client.post(url, review, format='json')
    assert resp.status_code == HTTP_201_CREATED
    assert Review.objects.count() == 1
