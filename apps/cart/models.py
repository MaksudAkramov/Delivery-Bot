from django.db import models
from datetime import datetime

from apps.bot.models import BotUser
from apps.product.models import Product

class Cart(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return str(self.user)

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return str(self.product.name)


