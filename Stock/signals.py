# Bad product signals 
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from Branch.models import Branch_Product
from Stock.models import Stock


@receiver(pre_save, sender=Stock)
def stock_added(sender, instance, *args, **kwargs):          
    try: 
        branch_product =  Branch_Product.objects.get(branch = instance.branch,
                                                        product = instance.product )
        if instance.pk:
            old_instance = Stock.objects.get(pk=instance.pk)
            diff = instance.qty - old_instance.qty 
            branch_product.current_qty += diff
            branch_product.save()  
        else: 
            branch_product.current_qty += instance.qty
            branch_product.save()     
    except Branch_Product.DoesNotExist:
        Branch_Product.objects.create(branch = instance.branch, 
                                         product = instance.product,
                                         current_qty = instance.qty)
        
@receiver(post_delete, sender=Stock)
def stock_deleted(sender, instance, *args, **kwargs):          
    try: 
        branch_product =  Branch_Product.objects.get(branch = instance.branch,
                                                        product = instance.product )
        branch_product.current_qty -= instance.qty
        branch_product.save()     
    except Branch_Product.DoesNotExist:
        pass
       