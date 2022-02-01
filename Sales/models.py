from django.db import models
from Branch.models import Branch
from Product.models import Product

# Create your models here.

class Items(models.Model):
    """Model definition for Items."""
    product = models.ForeignKey(Product, verbose_name="product", 
                    related_name="selected_product", on_delete=models.CASCADE)
    qty = models.IntegerField("qty")
    unit_price = models.DecimalField("unit_price", max_digits=10, decimal_places=2)
    total_price = models.DecimalField("total_price", max_digits=10, decimal_places=2)


    # TODO: Define fields here

    class Meta:
        """Meta definition for Items."""

        verbose_name = 'Items'
        verbose_name_plural = 'Items'

    def __str__(self):
        """Unicode representation of Items."""
        return self.product


class Sales(models.Model):
    """Model definition for Sales."""
    CHANNEL_CHOICES = (
        ('web', 'web'),
        ('store', 'store'),
    )
    PAYMENT_CHOICES = (
        ('transfer', 'transfer'),
        ('cash', 'cash'),
        ('online', 'online'),
    )

    # TODO: Define fields here
    branch = models.ForeignKey(Branch,related_name="sales_branch", verbose_name="branch", on_delete=models.CASCADE)
    total_amount = models.DecimalField("total_amount", max_digits=10, decimal_places=2)
    remark = models.CharField("remark", max_length=200)
    channel = models.CharField("channel", max_length=5, choices=CHANNEL_CHOICES)
    payment_method = models.CharField("payment_method", max_length=8, choices=PAYMENT_CHOICES)
    customer_name = models.CharField("customer_name", max_length=200, blank=True, null= True)
    phone_number = models.CharField("phone_number", max_length=20, null = False,blank=False)
    email = models.EmailField("email", max_length=254)
    address = models.CharField("address", max_length=254)
    date = models.DateField("date", auto_now=False, auto_now_add=True)
    items = models.ManyToManyField(Items, verbose_name="items",related_name="items")

    class Meta:
        """Meta definition for Sales."""

        verbose_name = 'Sales'
        verbose_name_plural = 'Sales'

    def __str__(self):
        """Unicode representation of Sales."""
        return f"{self.phone_number} - {str(self.total_amount)}"



