import pytest
from model_bakery import baker


@pytest.fixture
def order_factory():
    def factory(**kwargs):
        return baker.make("Order", **kwargs)

    return factory
