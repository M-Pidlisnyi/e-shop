from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)


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
