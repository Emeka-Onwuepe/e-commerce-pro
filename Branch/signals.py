from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete, m2m_changed

import Branch
from Branch.models import Branch



# @receiver(m2m_changed, sender=Branch.branch_products.through)
# def branch_products_changes(sender, instance,action,reverse,model,pk_set,**kwargs):
#     print(action)
#     if action == "post_add":
#         print(pk_set)
          
          