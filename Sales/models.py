from django.db import models
from django.forms import BooleanField
from Branch.models import Branch
from Product.models import Product, Size
from User.models import Customer

# Create your models here.

class Items(models.Model):
    """Model definition for Items."""
    product = models.ForeignKey(Product, verbose_name="product", 
                    related_name="selected_product", on_delete=models.CASCADE)
    product_type = models.CharField('product_type', max_length = 200)
    size  = models.CharField('size', max_length = 200)
    size_instance = models.ForeignKey(Size, verbose_name="size_instance", on_delete=models.CASCADE,
                        related_name="items_size_instance",null=True, blank=True)
    color = models.CharField('color', max_length = 200)
    qty = models.IntegerField("qty")
    unit_price = models.DecimalField("unit_price", max_digits=10, decimal_places=2)
    total_price = models.DecimalField("total_price", max_digits=10, decimal_places=2)
    mini_price = models.DecimalField("mini_price", max_digits=10, decimal_places=2)
    expected_price = models.DecimalField("expected_price", max_digits=10, decimal_places=2)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Items."""

        verbose_name = 'Items'
        verbose_name_plural = 'Items'

    def __str__(self):
        """Unicode representation of Items."""
        return f"{self.product_type} - {str(self.total_price)}"


class Sales(models.Model):
    """Model definition for Sales."""
    CHANNEL_CHOICES = (
        ('web', 'web'),
        ('store', 'store'),
    )
    PAYMENT_CHOICES = (
        ('transfer', 'transfer'),
        ('cash', 'cash'),
        ('credit', 'credit'),
    )

    # TODO: Define fields here
    branch = models.ForeignKey(Branch,related_name="sales_branch", verbose_name="branch", on_delete=models.CASCADE)
    total_amount = models.DecimalField("total_amount", max_digits=10, decimal_places=2)
    expected_amount = models.DecimalField("expected_amount", max_digits=10, decimal_places=2)
    remark = models.CharField("remark", max_length=200)
    channel = models.CharField("channel", max_length=5, choices=CHANNEL_CHOICES)
    payment_method = models.CharField("payment_method", max_length=8, choices=PAYMENT_CHOICES)
    date = models.DateField("date", auto_now=False, auto_now_add=True)
    customer = models.ForeignKey(Customer, verbose_name="customer",related_name="sales_customer",on_delete=models.CASCADE)
    items = models.ManyToManyField(Items, verbose_name="items",related_name="items")
    purchase_id = models.CharField("purchase_id", max_length=150)
    paid = models.BooleanField("paid",default=True)
    paid = models.BooleanField("paid",default=True)

    
    

    class Meta:
        """Meta definition for Sales."""

        verbose_name = 'Sales'
        verbose_name_plural = 'Sales'

    def __str__(self):
        """Unicode representation of Sales."""
        return f"{self.purchase_id} - {str(self.total_amount)}"



