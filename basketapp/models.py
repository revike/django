from django.conf import settings
from django.db import models
from mainapp.models import Product


# class BasketQuerySet(models.QuerySet):

#     def delete(self, *args, **kwargs):
#         for object in self:
#             object.product.quantity += object.quantity
#             object.product.save()
#         super().delete(*args, **kwargs)


class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(
        auto_now_add=True, verbose_name='время')

    @property
    def product_cost(self):
        return self.quantity * self.product.price

    @property
    def total_quantity(self):
        """Общее количество"""
        _items = Basket.objects.filter(user=self.user)
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    @property
    def total_cost(self):
        """Общая сумма"""
        _items = Basket.objects.filter(user=self.user)
        _total_cost = sum(list(map(lambda x: x.product_cost, _items)))
        return _total_cost

    # def delete(self):
    #     self.product.quantity += self.quantity
    #     self.product.save()

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)
