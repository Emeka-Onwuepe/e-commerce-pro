from django.db.models.signals import pre_save, post_delete,m2m_changed
from django.dispatch import receiver
from Branch.models import Branch, Branch_Product

from Product.models import Product

@receiver(m2m_changed, sender=Product.branches.through)
def branch_products_changes(sender, instance,action,reverse,model,pk_set,**kwargs):
    print(action)
    if action == "post_add":
        print("hello")
        for branch_id in pk_set:
           try:
               Branch_Product.objects.get(branch = branch_id, product = instance.id )
           except Branch_Product.DoesNotExist:
               branch = Branch.objects.get(pk=branch_id)
               Branch_Product.objects.create(branch = branch, product = instance )
               
           