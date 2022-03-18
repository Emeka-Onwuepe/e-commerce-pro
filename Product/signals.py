from django.db.models.signals import pre_save, post_save, post_delete,m2m_changed
from django.dispatch import receiver
from Branch.helper import manageBranchProducts, update_branch_Product_on_delete
from Branch.models import Branch, Branch_Product, Multiple_Size
from Product.models import Bad_Product, Product, Returned_Product

# products signals
@receiver(pre_save, sender=Product)
def update_Product_image(sender, instance, *args, **kwargs):
    if instance.pk:
        product = Product.objects.get(pk=instance.pk)
        if product.image != instance.image:
            product.image.delete(False)
            
    
@receiver(post_delete, sender=Product)
def delete_product_image(sender, instance, using, *args, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
            
@receiver(m2m_changed, sender=Product.multipleSIzes.through)
def product_multipleSIzes_changes(sender, instance,action,reverse,model,pk_set,**kwargs):
    if action == "post_add":
         if instance.multipleSIzes.exists():
            instance.price = 0
            instance.size = 0
            instance.save()
               
@receiver(m2m_changed, sender=Product.branches.through)
def product_branch_changes(sender, instance,action,reverse,model,pk_set,**kwargs):
    if action == "post_add":
        if instance.multipleSIzes.exists():
            for branch_id in pk_set:
                try:
                    Branch_Product.objects.get(branch = branch_id, product = instance.id,
                                          is_multiple_sized = True )
                except Branch_Product.DoesNotExist: 
                    branch = Branch.objects.get(pk=branch_id)
                    branch_product = Branch_Product.objects.create(branch = branch,
                                                              product = instance,is_multiple_sized = True)
                    for size in instance.multipleSIzes.all():
                       try:
                           Multiple_Size.objects.get(branch_product = branch_product.id,
                                                     size = size.id)
                       except Multiple_Size.DoesNotExist:
                           Multiple_Size.objects.create(branch_product = branch_product,
                                                     size = size) 
        else:
            for branch_id in pk_set:
               try:
                    Branch_Product.objects.get(branch = branch_id, product = instance.id,
                                          is_multiple_sized = False )
               except Branch_Product.DoesNotExist:
                    branch = Branch.objects.get(pk=branch_id)
                    branch_product = Branch_Product.objects.create(branch = branch,
                                                              product = instance )
        
                            
# Bad product signals 
@receiver(pre_save, sender=Bad_Product)
def bad_product_added(sender, instance, *args, **kwargs):
    manageBranchProducts(instance,Bad_Product,"bad_qty")          
        
@receiver(post_delete, sender=Bad_Product)
def bad_product_deleted(sender, instance, *args, **kwargs): 
    update_branch_Product_on_delete(instance,"bad_qty")
        
       
# returned product signals
@receiver(pre_save, sender=Returned_Product)
def returned_product_added(sender, instance, *args, **kwargs):
    manageBranchProducts(instance,Returned_Product,"returned_qty")           
    
        
@receiver(post_delete, sender=Returned_Product)
def returned_product_deleted(sender, instance, *args, **kwargs):          
    update_branch_Product_on_delete(instance,"returned_qty")
       