import pytest
from model_bakery import baker


@pytest.fixture
def review_factory():
    def factory(**kwargs):
        return baker.make("Review", **kwargs)

    return factory


@pytest.fixture
def product_factory():
    def factory(**kwargs):
        return baker.make("Product", **kwargs)

    return factory
