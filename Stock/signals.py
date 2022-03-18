# Bad product signals 
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from Branch.helper import manageBranchProducts, update_branch_Product_on_delete
from Stock.models import Stock


@receiver(pre_save, sender=Stock)
def stock_added(sender, instance, *args, **kwargs):
    manageBranchProducts(instance,Stock,"current_qty") 

        
@receiver(post_delete, sender=Stock)
def stock_deleted(sender, instance, *args, **kwargs): 
    update_branch_Product_on_delete(instance,"current_qty")