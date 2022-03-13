from django.db import models

from Branch.models import Branch
# Create your models here.

class Category(models.Model):
    """Model definition for Category."""

    # TODO: Define fields here
    name = models.CharField("Category",max_length = 150,null=False,blank=False)
    
    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """Unicode representation of Category."""
        return self.name


class Product_Type(models.Model):
    """Model definition for Product_Type."""

    # TODO: Define fields here
    name = models.CharField("name",max_length = 200,null=False,blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="category")
    
    class Meta:
        """Meta definition for Product_Type."""

        verbose_name = 'Product_Type'
        verbose_name_plural = 'Product_Types'

    def __str__(self):
        """Unicode representation of Product_Type."""
        return f"{self.category} - {self.name}"


class Size(models.Model):
    """Model definition for Size."""

    size = models.CharField(verbose_name="size", max_length=150)
    price = models.IntegerField(verbose_name="price")
    description = models.CharField(verbose_name="description", max_length=150)

    class Meta:
        """Meta definition for Size."""

        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'

    def __str__(self):
        """Unicode representation of Topping."""
        return f' {self.description}-{self.size}-{self.price}'
    
class Product(models.Model):
    """Model definition for Product."""

    # TODO: Define fields here
    product_type = models.ForeignKey(Product_Type, on_delete=models.CASCADE, related_name="product_type")
    size = models.CharField(verbose_name="size",default="0", max_length=150,null=True,blank=True)
    description = models.TextField(verbose_name="description", max_length=150,null=False,blank=False)
    multipleSIzes = models.ManyToManyField(
        Size, verbose_name="multiplesizes", related_name="multiplesizes", blank=True)
    color = models.CharField("color",max_length = 200,null=False,blank=False)
    image = models.ImageField(verbose_name="image", default="image",null=True,blank=True)
    price = models.DecimalField("price", max_digits=50,default=0, decimal_places=2,null=True,blank=True)
    publish = models.BooleanField(default=False)
    branches = models.ManyToManyField(Branch, verbose_name="branches",related_name="products_branches",blank=True)

    class Meta:
        """Meta definition for Product."""

        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        """Unicode representation of Product."""
        return f"{self.product_type} - {self.color} - {self.size}"


class Bad_Product(models.Model):
    """Model definition for Bad_Product."""

    # TODO: Define fields here
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name = "bad_product_product_type")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="bad_product_branch")
    qty = models.IntegerField("qty",null=False,blank=False)
    date = models.DateField("date", auto_now=False, auto_now_add=True)
    
    class Meta:
        """Meta definition for Bad_Product."""

        verbose_name = 'Bad_Product'
        verbose_name_plural = 'Bad_Products'
        ordering = ['-date']

    def __str__(self):
        """Unicode representation of Bad_Product."""
        return f'{self.branch} - {self.product} ({self.date})'

class Returned_Product(models.Model):
    """Model definition for Returned_Product."""

    # TODO: Define fields here
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name = "returned_product_product_type")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="returned_product_branch")
    qty = models.IntegerField("qty",null=False,blank=False)
    unit_price = models.DecimalField("unit_price", max_digits=6, decimal_places=2,null=False,blank=False)
    total_price = models.DecimalField("total_price", max_digits=6, decimal_places=2,null=False,blank=False) 
    date_of_purchase = models.DateField("date_of_purchase", auto_now=False, auto_now_add=False,null=False,blank=False)
    date_of_return = models.DateTimeField("date_of_return", auto_now=False, auto_now_add=False,null=False,blank=False)

    class Meta:
        """Meta definition for Returned_Product."""

        verbose_name = 'Returned_Product'
        verbose_name_plural = 'Returned_Products'

    def __str__(self):
        """Unicode representation of Returned_Product."""
        return f" {self.branch} - {self.product} - {self.total_price}"
