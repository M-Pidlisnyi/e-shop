from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
import uuid
from decimal import Decimal
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def get_absolute_url(self):
        return f"/catalogue/category/{self.id}"


class Product(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    quantity = models.IntegerField()
    IN_STOCK = "IS"
    NOT_IN_STOCK = "NIS"
    DISCONTINUED = "DIS"
    ON_SALE = "OS"
    STATUS = {
        IN_STOCK: "In stock",
        NOT_IN_STOCK: "Temporarily unavailable",
        DISCONTINUED: "No longer available",
        ON_SALE: "In stock. Great Price!"
    }
    status = models.CharField(max_length=25, choices=STATUS.items(), default=IN_STOCK)
    description = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        return f"/catalogue/products/{self.id}"

    def __str__(self):
        return f"{self.name}({self.id}) - {self.category.name}({self.category.id})"

    class Meta:
        db_tablespace = "catalogue"
        indexes = [
            models.Index(fields=["price"], name="price_index")
        ]


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    discount_card_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    discount_value = models.DecimalField(max_digits=100, decimal_places=2, default=0.99)
    order_history = models.ManyToManyField(Product, through="Order")

    class Meta:
        verbose_name = "Shop Customer"
        verbose_name_plural = "Shop Customers"

    def __str__(self):
        return f"{self.user.username} card No.{self.discount_card_number}"

    @property
    def max_discount(self):
        if self.user.is_staff:
            return 99
        return 50


    def update_discount(self):
        if self.discount_value < self.max_discount:
            self.discount_value += Decimal(0.01)
            self.save()


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_DEFAULT, default="deleted product")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)# when customer is deleted we want to delete history of purchases
    amount = models.IntegerField()
    price_with_discount = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.customer.user.username} bought {self.amount} of {self.product} at {self.datetime} for {self.price_with_discount}"

    class Meta:
        ordering = ["-datetime"]
        db_tablespace = "catalogue"
        indexes = [
            models.Index(fields=["price_with_discount"], name="price_with_discount_index")
        ]
        constraints = [
            models.CheckConstraint(check=Q(amount__gt=0), name="amount greater than 0", violation_error_message="Amount must be greater than zero")
        ]