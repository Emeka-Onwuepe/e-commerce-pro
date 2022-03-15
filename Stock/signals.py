# Bad product signals 
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from Branch.models import Branch_Product, Multiple_Size
from Stock.models import Stock


@receiver(pre_save, sender=Stock)
def stock_added(sender, instance, *args, **kwargs): 
    if instance.size:         
        try: 
            branch_product =  Branch_Product.objects.get(branch = instance.branch,
                                                            product = instance.product,
                                                            is_multiple_sized = True )
            try:
                multiple_size = Multiple_Size.objects.get(branch_product = branch_product.id,
                                                     size = instance.size)
                if instance.pk:
                    old_instance = Stock.objects.get(pk=instance.pk)
                    diff = instance.qty - old_instance.qty 
                    multiple_size.current_qty += diff
                    multiple_size.save()  
                else: 
                    multiple_size.current_qty += instance.qty
                    multiple_size.save()   
                
            except Multiple_Size.DoesNotExist:
                
                Multiple_Size.objects.create(branch_product = branch_product,
                                             size = instance.size,
                                            current_qty = instance.qty)
             
        except Branch_Product.DoesNotExist:
            branch_product = Branch_Product.objects.create(branch = instance.branch, 
                                            product = instance.product,
                                            current_qty = instance.qty)
            Multiple_Size.objects.create(branch_product = branch_product,
                                             size = instance.size,
                                            current_qty = instance.qty)
    else:
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
    if instance.size:
        try: 
            branch_product =  Branch_Product.objects.get(branch = instance.branch,
                                                            product = instance.product )
            try:
                multiple_size = Multiple_Size.objects.get(branch_product = branch_product.id,
                                                     size = instance.size)
                multiple_size.current_qty -= instance.qty
                multiple_size.save() 
            except Multiple_Size.DoesNotExist:
                pass      
        except Branch_Product.DoesNotExist:
            pass
    else:         
        try: 
            branch_product =  Branch_Product.objects.get(branch = instance.branch,
                                                            product = instance.product )
            branch_product.current_qty -= instance.qty
            branch_product.save()     
        except Branch_Product.DoesNotExist:
            pass
       