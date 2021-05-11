import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_201_CREATED
from my_shop_app.models import Collection


# список коллекций
@pytest.mark.django_db
def test_get_collections(unauthorized_client):
    url = reverse('collections-list')
    resp = unauthorized_client.get(url)
    assert resp.status_code == HTTP_200_OK


# создание коллекции товаров авторизованным пользователем
@pytest.mark.django_db
def test_create_collection_admin(admin_client, api_client, product_factory):
    url = reverse('collections-list')
    product1 = product_factory()
    product2 = product_factory()
    collection = {
        "title": "Collection 1",
        "text": "Apple iPhone 12 Pro Max + Watch",
        "collections": [
            {
                "product_id": product1.id
            },
            {
                "product_id": product2.id
            }
        ]
    }
    resp = api_client.post(url, collection, format='json')
    assert resp.status_code == HTTP_403_FORBIDDEN
    assert Collection.objects.count() == 0

# создание коллекции товаров админом
    resp = admin_client.post(url, collection, format='json')
    assert resp.status_code == HTTP_201_CREATED
    assert Collection.objects.count() == 1


