from django.db.models.signals import pre_delete,post_delete,m2m_changed
from django.dispatch import receiver
from Branch.models import Branch_Product, Multiple_Size
from Sales.models import Items, Sales


@receiver(m2m_changed, sender= Sales.items.through)
def sales_multipleSIzes_changes(sender, instance,action,reverse,model,pk_set,**kwargs):
    if action == "post_add":
        for item_id in pk_set:
            item = Items.objects.get(pk=item_id)
            try:
                branch_product =  Branch_Product.objects.get(branch = instance.branch,
                                                            product = item.product,
                                                            is_multiple_sized = True )
                try:
                    multiple_size = Multiple_Size.objects.get(branch_product = branch_product.id,
                                                size = item.size_instance)
                    multiple_size.current_qty -= item.qty
                    multiple_size.save() 
                    
                    
                except Multiple_Size.DoesNotExist:
                    multiple_size = Multiple_Size.objects.create(branch_product = branch_product,
                                                size = item.size_instance)
                    multiple_size.current_qty -= item.qty
                    multiple_size.save()
            except Branch_Product.DoesNotExist:
                branch_product =  Branch_Product.objects.create(branch = instance.branch,
                                                            product = item.product,
                                                            is_multiple_sized = True )
                multiple_size = Multiple_Size.objects.create(branch_product = branch_product,
                                                size = item.size_instance)
                multiple_size.current_qty -= item.qty
                multiple_size.save()
                
                

@receiver(pre_delete, sender=Sales)
def delete_sale(sender, instance, *args, **kwargs):
    for item in instance.items.all():
        try:
            branch_product =  Branch_Product.objects.get(branch = instance.branch,
                                                            product = item.product,
                                                            is_multiple_sized = True )
            try:
                multiple_size = Multiple_Size.objects.get(branch_product = branch_product.id,
                                                size = item.size_instance)
                multiple_size.current_qty += item.qty
                multiple_size.save() 
                    
                    
            except Multiple_Size.DoesNotExist:
                multiple_size = Multiple_Size.objects.create(branch_product = branch_product,
                                                size = item.size_instance)
                multiple_size.current_qty += item.qty
                multiple_size.save()
        except Branch_Product.DoesNotExist:
            branch_product =  Branch_Product.objects.create(branch = instance.branch,
                                                            product = item.product,
                                                            is_multiple_sized = True )
            multiple_size = Multiple_Size.objects.create(branch_product = branch_product,
                                                size = item.size_instance)
            multiple_size.current_qty += item.qty
            multiple_size.save()
