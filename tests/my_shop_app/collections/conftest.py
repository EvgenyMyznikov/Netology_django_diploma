import pytest
from model_bakery import baker


@pytest.fixture
def product_factory():
    def factory(**kwargs):
        return baker.make("Product", **kwargs)

    return factory
