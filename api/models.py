import uuid

from django.db import models


class Fridge(models.Model):
    account = models.CharField(primary_key=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.account


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    image = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class FridgeProduct(models.Model):
    fridge = models.ForeignKey(Fridge, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()

    class Meta:
        unique_together = [['fridge', 'product']]

    def __str__(self):
        return str(self.id)


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "pending"
        CHECKED = "CHECKED", "checked"
        PAYED = "PAYED", "payed"
        FAILED = "FAILED", "failed"

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class OrderProduct(models.Model):
    fridge_product = models.ForeignKey(FridgeProduct, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    amount = models.IntegerField()

    class Meta:
        unique_together = [['fridge_product', 'order']]

    def __str__(self):
        return str(self.id)


class Transaction(models.Model):
    prv_txn_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    check_txn_id = models.UUIDField(null=True, blank=True)
    pay_txn_id = models.UUIDField(null=True, blank=True)
    txn_date = models.CharField(null=True, blank=True)

    def __str__(self):
        return str(self.prv_txn_id)



