from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    company = models.CharField(null=True, blank=True, max_length=255)
    is_local_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Fridge(models.Model):
    owner = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    account = models.CharField(primary_key=True)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.account


class CourierFridgePermission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fridge = models.ForeignKey(Fridge, on_delete=models.PROTECT)


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    image = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class FridgeProduct(models.Model):
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['fridge', 'product']]

    def __str__(self):
        return str(self.id)

    def reduce_quantity(self, amount):
        self.quantity -= amount
        self.save()


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "pending"
        CHECKED = "CHECKED", "checked"
        SUCCESS = "SUCCESS", "success"
        FAILED = "FAILED", "failed"

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def set_status(self, new_status):
        self.status = new_status
        self.save()

    def set_date(self, date):
        self.date = date
        self.save()

    def calculate_total_sum(self) -> int:
        order_products = self.orderproduct_set.all()

        total_sum: int = 0
        for order_product in order_products:
            total_sum += order_product.fridge_product.product.price * order_product.amount

        return total_sum

    def calculate_product_quantity(self) -> int:
        order_products = self.orderproduct_set.all()
        return len(order_products)


class OrderProduct(models.Model):
    fridge_product = models.ForeignKey(FridgeProduct, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()

    class Meta:
        unique_together = [['fridge_product', 'order']]

    def __str__(self):
        return str(self.id)


class Transaction(models.Model):
    order = models.OneToOneField(Order, on_delete=models.PROTECT)
    check_txn_id = models.CharField(null=True, blank=True)
    pay_txn_id = models.CharField(null=True, blank=True)
    txn_date = models.CharField(null=True, blank=True)
    expiration_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def set_check_txn_id(self, check_txn_id):
        self.check_txn_id = check_txn_id
        self.save()

    def set_pay_txn_id_and_date(self, pay_txn_id, txn_date):
        self.pay_txn_id = pay_txn_id
        self.txn_date = txn_date
        self.save()


class Token(models.Model):
    email = models.EmailField(max_length=255)
    code = models.CharField(max_length=6, unique=True)
    token = models.CharField(max_length=55, unique=True, default=None, blank=True, null=True)
    expiration_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.email} - {self.token}"
