from django.db import models
from Product.models import Product
from User.models import Customer

# Create your models here.
class Pre_Order(models.Model):
    """Model definition for Pre_Order."""

    # TODO: Define fields here
    product = models.ForeignKey(Product, verbose_name="pre_ordered_product", 
                on_delete=models.CASCADE, related_name="pre_ordered_product")
    customer = models.ForeignKey(Customer, verbose_name="pre_ordered_customer", 
                on_delete=models.CASCADE, related_name="pre_ordered_customer")
    qty = models.IntegerField("qty",blank=False)
    archive = models.BooleanField("archive",default=False) 
    date = models.DateField("date", auto_now=False, auto_now_add=True)   

    class Meta:
        """Meta definition for Pre_Order."""

        verbose_name = 'Pre_Order'
        verbose_name_plural = 'Pre_Orders'

    def __str__(self):
        """Unicode representation of Pre_Order."""
        return f'{self.customer} - {self.product} - {self.qty}'
