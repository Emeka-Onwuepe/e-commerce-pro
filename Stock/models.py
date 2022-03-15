from django.db import models
from Branch.models import Branch
from Product.models import Product, Size, Size

# Create your models here.
   
class Stock(models.Model):
    """Model definition for Stock."""

    # TODO: Define fields here
    qty = models.IntegerField("qty", null=False, blank=False)
    product = models.ForeignKey(Product, verbose_name="product", on_delete=models.CASCADE,
                        related_name="stock_product")
    branch = models.ForeignKey(Branch, verbose_name="branch", on_delete=models.CASCADE,
                        related_name="stock_branch")
    size = models.ForeignKey(Size, verbose_name="size", on_delete=models.CASCADE,
                        related_name="size_branch",null=True, blank=True)
    date = models.DateTimeField("date",auto_now_add=True)

    class Meta:
        """Meta definition for Stock."""

        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'

    def __str__(self):
        """Unicode representation of Stock."""
        return f'{self.branch} - {self.product} - ({self.qty})'
