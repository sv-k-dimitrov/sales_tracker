from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class SalesRecord(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.IntegerField()
    total_sales_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_sale = models.DateTimeField()

    def __str__(self):
        return f'{self.product.name} - {self.quantity_sold} sold on {self.date_of_sale}'
