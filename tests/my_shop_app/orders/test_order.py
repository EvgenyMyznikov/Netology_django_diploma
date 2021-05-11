import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED

from tests.my_shop_app.test_product import test_create_product_admin
from my_shop_app.models import Order


@pytest.mark.django_db
def test_create_user():
    User.objects.create_user('testuser', 'testuser@email.com', 'user12345')
    assert User.objects.count() == 1


# получение списка всех заказов админом
@pytest.mark.django_db
def test_list_order(admin_client, order_factory):
    url = reverse('orders-list')
    order1 = order_factory()
    order2 = order_factory()
    resp = admin_client.get(url)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert len(resp_json) == 2
    resp_ids = {elem['id'] for elem in resp_json}
    assert resp_ids == {order1.id, order2.id}


# создание заказа неавторизованным пользователем
@pytest.mark.django_db
def test_create_order_unauthorized(unauthorized_client, api_client, admin_client):
    url = reverse('orders-list')
    product = test_create_product_admin(admin_client)
    order = {
        "positions": [
            {
                "product": product['id'],
                "quantity": 1
            },
        ]
    }
    resp = unauthorized_client.post(url, order, format='json')
    assert resp.status_code == HTTP_401_UNAUTHORIZED
    assert Order.objects.count() == 0


# создание заказа авторизованным пользователем
@pytest.mark.django_db
def test_create_order_user(api_client, admin_client):
    url = reverse('orders-list')
    product = test_create_product_admin(admin_client)
    order = {
        "positions": [
            {
                "product": product['id'],
                "quantity": 1
            },
        ]
    }
    resp = api_client.post(url, order, format='json')
    assert resp.status_code == HTTP_201_CREATED
    assert Order.objects.count() == 1


# получение списка своих заказов авторизованным пользователем
@pytest.mark.django_db
def test_list_order_buyer(api_client, order_factory):
    url = reverse('orders-list')
    order_factory(buyer=User.objects.get(username='testuser'))
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK


# изменение статуса заказа авторизованным пользователем
@pytest.mark.django_db
def test_update_status_order_user(api_client, order_factory):
    order = order_factory(buyer=User.objects.get(username='testuser'))
    url = reverse("orders-detail", args=[order.id])
    resp = api_client.patch(url, {
        "order_status": "2"
    })
    assert resp.status_code == HTTP_403_FORBIDDEN


# изменение статуса заказа админом
@pytest.mark.django_db
def test_update_status_order_user(admin_client, order_factory):
    order = order_factory(buyer=User.objects.get(username='admin'))
    url = reverse("orders-detail", args=[order.id])
    resp = admin_client.patch(url, {
        "order_status": "2"
    })
    assert resp.status_code == HTTP_200_OK
