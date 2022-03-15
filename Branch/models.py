from django.db import models

# Create your models here.

class Branch(models.Model):
    """Model definition for Branch."""

    # TODO: Define fields here
    name = models.CharField('Branch Name', max_length = 200)

    class Meta:
        """Meta definition for Branch."""

        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'

    def __str__(self):
        """Unicode representation of Branch."""
        return self.name


class Branch_Product(models.Model):
    """Model definition for Branch_Product."""

    # TODO: Define fields here
    branch = models.ForeignKey(Branch, verbose_name="branch", 
                on_delete=models.CASCADE, related_name="branch_product_branch")  
    product = models.ForeignKey("Product.Product", verbose_name="product", 
                on_delete=models.CASCADE, related_name="branch_product_product") 
    is_multiple_sized = models.BooleanField("is_multiple_sized",default=False)
    current_qty = models.IntegerField("current_qty", default=0)
    returned_qty = models.IntegerField("returned_qty", default=0)
    bad_qty = models.IntegerField("bad_qty", default=0)


    class Meta:
        """Meta definition for Branch_Product."""

        verbose_name = 'Branch_Product'
        verbose_name_plural = 'Branch_Products'

    def __str__(self):
        """Unicode representation of Branch_Product."""
        return f'{self.branch} - {self.product}'
    

class Multiple_Size(models.Model):
    """Model definition for multiple_size."""

    # TODO: Define fields here
    branch_product = models.ForeignKey(Branch_Product, verbose_name="multiple_size_branch_product",
                                       on_delete=models.CASCADE)
    size = models.ForeignKey("Product.Size", related_name='branch_product_sizes',
                             on_delete=models.CASCADE)
    current_qty = models.IntegerField("current_qty", default=0)
    returned_qty = models.IntegerField("returned_qty", default=0)
    bad_qty = models.IntegerField("bad_qty", default=0)

    class Meta:
        """Meta definition for multiple_size."""

        verbose_name = 'multiple_size'
        verbose_name_plural = 'multiple_sizes'

    def __str__(self):
        """Unicode representation of multiple_size."""
        return f'{self.branch_product} - {self.size}'
