from django.contrib.auth.models import User
from django.db import models
from rest_framework.authtoken.models import Token


class Product(models.Model):
    """Товар"""

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    name = models.CharField(max_length=250, verbose_name='Наименование')
    description = models.TextField(max_length=1000, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, verbose_name='Цена', decimal_places=2)
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлен', auto_now=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзыв к товару"""

    RATINGS = (
        ('1', '1 Star'),
        ('2', '2 Stars'),
        ('3', '3 Stars'),
        ('4', '4 Stars'),
        ('5', '5 Stars'),
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    author_id = models.ForeignKey('auth.User', related_name='review_author', verbose_name='Автор',
                                  on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, related_name='reviews', verbose_name='Товар', on_delete=models.CASCADE)
    rating = models.CharField(verbose_name='Рейтинг товара', max_length=1, choices=RATINGS, blank=True, default=None)
    text = models.TextField(verbose_name='Текст отзыва')
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлен', auto_now=True)

    def __str__(self):
        return f"Отзыв о товаре: {self.product_id} автор: {self.author_id}"


class ProductOrderPosition(models.Model):
    """Товары в заказе и их количество"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', related_name='positions', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество единиц товара')


class Order(models.Model):
    """Заказы"""

    STATUSES = (
        ('1', 'NEW'),
        ('2', 'IN_PROGRESS'),
        ('3', 'DONE')
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    buyer = models.ForeignKey('auth.User', related_name="order", verbose_name='Покупатель', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through=ProductOrderPosition)
    order_status = models.CharField(max_length=30, verbose_name='Статус заказа', choices=STATUSES, default='1')
    order_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость заказа', default=0)
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлен', auto_now=True)

    def __str__(self):
        return f"Заказ № {self.id} на сумму {self.order_price}"


class ProductCollection(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    collection = models.ForeignKey('Collection', related_name='collections', on_delete=models.CASCADE)


class Collection(models.Model):
    """Подборка товаров"""

    class Meta:
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'

    title = models.TextField(verbose_name='Заголовок')
    text = models.TextField(verbose_name='Описание подборки товаров')
    products_in_collection = models.ManyToManyField(Product, through=ProductCollection)
    created_at = models.DateTimeField(verbose_name='Создана', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлена', auto_now=True)

    def __str__(self):
        return self.title
