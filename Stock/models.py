from django.db import models
from Branch.models import Branch_Product

# Create your models here.
   
class Stock(models.Model):
    """Model definition for Stock."""

    # TODO: Define fields here
    qty = models.IntegerField("qty", null=False, blank=False)
    branch_product = models.ForeignKey(Branch_Product, verbose_name="branch_product", on_delete=models.CASCADE,
                        related_name="stock_branch_product")
    date = models.DateTimeField("date",auto_now_add=True)

    class Meta:
        """Meta definition for Stock."""

        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'

    def __str__(self):
        """Unicode representation of Stock."""
        return self.branch_product

