from django.db.models.signals import pre_save,pre_delete,post_delete,m2m_changed
from django.dispatch import receiver
from Branch.models import Branch_Product, Multiple_Size
from Credit_Sales.models import Credit_Sale, Payment
from Sales.models import Items

@receiver(m2m_changed, sender= Credit_Sale.items.through)
def credit_sales_multipleSIzes_changes(sender, instance,action,reverse,model,pk_set,**kwargs):
    if action == "post_add":
        for item_id in pk_set:
            item = Items.objects.get(pk=item_id)
            if item.size_instance:        
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
                    branch_product = Branch_Product.objects.create(branch = instance.branch, 
                                                    product = item.product,
                                                    current_qty = instance.qty,
                                                    is_multiple_sized = True)
                    multiple_size = Multiple_Size.objects.create(branch_product = branch_product,
                                                    size = item.size_instance)
                    multiple_size.current_qty -= item.qty
                    multiple_size.save()
            else:
                try: 
                    branch_product =  Branch_Product.objects.get(branch = instance.branch,
                                                                    product = item.product,is_multiple_sized=False )
                    branch_product.current_qty -= item.qty
                    branch_product.save()    
                except Branch_Product.DoesNotExist:
                    branch_product =  Branch_Product.objects.create(branch = instance.branch, 
                                                    product = item.product)
                    branch_product.current_qty -= item.qty
                    branch_product.save() 
                
            

@receiver(pre_delete, sender=Credit_Sale)
def delete_credit_sale(sender, instance, *args, **kwargs):
    for item in instance.items.all():
        if item.size_instance:
            try: 
                branch_product =  Branch_Product.objects.get(branch = instance.branch,
                                                                product = item.product,is_multiple_sized=True )
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
        else:         
            try: 
                branch_product =  Branch_Product.objects.get(branch = instance.branch,
                                                                product = item.product,is_multiple_sized=False )  
                branch_product.current_qty += item.qty
                branch_product.save()  
            except Branch_Product.DoesNotExist:
                branch_product =  Branch_Product.objects.create(branch = instance.branch,
                                                                product = item.product,is_multiple_sized=False )  
                branch_product.current_qty += item.qty
                branch_product.save() 
         
@receiver(pre_save, sender=Credit_Sale)
def add_credit_sale(sender, instance, *args, **kwargs):
    if not instance.pk:
        instance.balance = instance.total_amount * -1
    if instance.total_payment  >= instance.total_amount:
        instance.fully_paid = True
    else:
        instance.fully_paid = False


# Payment signals 
@receiver(pre_save, sender=Payment)
def add_payment(sender, instance, *args, **kwargs):
    credit_sale = Credit_Sale.objects.get(pk=instance.credit_sale_id)
    if instance.pk:
        old_instance = Payment.objects.get(pk=instance.pk)
        diff = instance.amount - old_instance.amount
        credit_sale.total_payment += diff
        credit_sale.balance += diff
        credit_sale.save()
    else:
        credit_sale.total_payment += instance.amount
        credit_sale.balance += instance.amount
        credit_sale.save()
 
@receiver(pre_delete, sender=Payment)   
def delete_payment(sender, instance, *args, **kwargs):
    credit_sale = Credit_Sale.objects.get(pk=instance.credit_sale_id)
    credit_sale.total_payment -= instance.amount
    credit_sale.balance -= instance.amount
    credit_sale.save(False)