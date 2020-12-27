from mainapp.models import Product
from django.conf import settings
from django.db import models


class Order(models.Model):
    FORMING = 'FM'
    SEND_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUSES = (
        (FORMING, 'формируется'),
        (SEND_TO_PROCEED, 'отправлено в обработку'),
        (PROCEEDED, 'обработано'),
        (PAID, 'оплачено'),
        (READY, 'готово к выдаче'),
        (CANCEL, 'отменено'),
    )

    # user = models.ForeignKey(ShopUser, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='пользователь')
    status = models.CharField(
        max_length=3, choices=ORDER_STATUSES, default=FORMING, verbose_name='статус')
    is_active = models.BooleanField(default=True, verbose_name='активен')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='дата создания заказа')
    updated = models.DateTimeField(
        auto_now=True, verbose_name='дата обновления заказа')

    @property
    def get_total_quantity(self):
        """Общее количество"""
        _items = self.orderitems.select_related()
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    @property
    def get_total_cost(self):
        """Общая сумма"""
        _items = self.orderitems.select_related()
        _total_cost = sum(list(map(lambda x: x.product_cost, _items)))
        return _total_cost


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='orderitems', verbose_name='заказ')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='продукт')
    quantity = models.PositiveIntegerField(
        default=0, verbose_name='количество')

    @property
    def product_cost(self):
        return self.quantity * self.product.price
