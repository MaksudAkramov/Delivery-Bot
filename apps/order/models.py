from uuid import uuid4
from django.db import models


class OrderInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order_owner = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=25)
    date = models.CharField(max_length=50, null=True)
    created_at = models.TimeField(auto_now_add=True)
    address = models.CharField(max_length=300)
    order_items = models.TextField()

    def __str__(self) -> str:
        return str(self.id)
