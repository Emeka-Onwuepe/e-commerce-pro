from django.db import models
from Branch.models import Branch
from Sales.models import Items
from User.models import Customer

# Create your models here.
class Credit_Sale(models.Model):
    """Model definition for Credit_Sale."""

    # TODO: Define fields here
    branch = models.ForeignKey(Branch,related_name="credit_sale_branch", verbose_name="branch", on_delete=models.CASCADE)
    total_amount = models.DecimalField("total_amount", max_digits=10, decimal_places=2)
    expected_amount = models.DecimalField("expected_amount", max_digits=10, decimal_places=2)
    remark = models.CharField("remark", max_length=200)
    date = models.DateField("date", auto_now=False, auto_now_add=True)
    items = models.ManyToManyField(Items, verbose_name="items",related_name="credit_sale_Items")
    customer = models.ForeignKey(Customer, verbose_name="customer",related_name="credit_sale_customer",on_delete=models.CASCADE)
    purchase_id = models.CharField("purchase_id", max_length=150)
    total_payment = models.DecimalField("total_payment",max_digits=10, decimal_places=2,default=0)
    balance = models.DecimalField("balance",max_digits=10, decimal_places=2,default=0)
    fully_paid = models.BooleanField("fully_paid",default=False)

    class Meta:
        """Meta definition for Credit_Sale."""

        verbose_name = 'Credit_Sale'
        verbose_name_plural = 'Credit_Sales'
        ordering = ["-date"]

    def __str__(self):
        """Unicode representation of Credit_Sale."""
        return f"{self.customer} - {str(self.total_amount)}"


class Payment(models.Model):
    """Model definition for Payment."""

    # TODO: Define fields here
    amount = models.DecimalField("amount", max_digits=10, decimal_places=2)
    date = models.DateField("date", auto_now=False, auto_now_add=True)
    credit_sale  = models.ForeignKey(Credit_Sale,verbose_name="credit_sale",
                                     related_name="payment_credit_sale", on_delete=models.CASCADE)
    class Meta:
        """Meta definition for Payment."""

        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        """Unicode representation of Payment."""
        return f"{self.credit_sale} - {str(self.amount)}"
