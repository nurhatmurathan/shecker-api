from django.db import models


class Fridge(models.Model):
    account = models.CharField(primary_key=True)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=255)

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
    quantity = models.PositiveIntegerField(default=0)

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


class OrderProduct(models.Model):
    fridge_product = models.ForeignKey(FridgeProduct, on_delete=models.PROTECT)
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
