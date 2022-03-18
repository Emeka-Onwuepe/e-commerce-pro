from Branch.models import Branch_Product, Multiple_Size


def addBranchProduct(product):
    if product.multipleSIzes.exists():
        for branch in product.branches.all():
            try:
                Branch_Product.objects.get(branch = branch.id, product = product.id,
                                          is_multiple_sized = True )
            except Branch_Product.DoesNotExist: 
                branch_product = Branch_Product.objects.create(branch = branch,
                                                              product = product,is_multiple_sized = True)
                for size in product.multipleSIzes.all():
                    try:
                        Multiple_Size.objects.get(branch_product = branch_product.id,
                                                     size = size.id)
                    except Multiple_Size.DoesNotExist:
                        Multiple_Size.objects.create(branch_product = branch_product,
                                                     size = size)
        
    else:
        for branch in product.branches.all():
            try:
                Branch_Product.objects.get(branch = branch.id, product = product.id,
                                          is_multiple_sized = False )
            except Branch_Product.DoesNotExist:
                branch_product = Branch_Product.objects.create(branch = branch,
                                                              product = product )
     
     
     
def manageBranchProducts(instance,model,action):
    if instance.size_instance:        
        try: 
            branch_product =  Branch_Product.objects.get(branch = instance.branch,
                                                            product = instance.product,
                                                            is_multiple_sized = True )
            try:
                multiple_size = Multiple_Size.objects.get(branch_product = branch_product.id,
                                                     size = instance.size_instance)
                if instance.pk:
                    old_instance = model.objects.get(pk=instance.pk)
                    diff = instance.qty - old_instance.qty 
                    if action == "current_qty":
                        multiple_size.current_qty += diff
                        multiple_size.save()
                    elif action == "bad_qty":
                        multiple_size.bad_qty += diff
                        multiple_size.current_qty -= diff
                        multiple_size.save()
                    elif action == "returned_qty":
                        multiple_size.returned_qty += diff
                        multiple_size.current_qty +=diff
                        multiple_size.save()      
                else:  
                    if action == "current_qty":
                        multiple_size.current_qty += instance.qty
                        multiple_size.save()
                    elif action == "bad_qty":
                        multiple_size.bad_qty += instance.qty
                        multiple_size.current_qty -= instance.qty
                        multiple_size.save()
                    elif action == "returned_qty":
                        multiple_size.returned_qty += instance.qty
                        multiple_size.current_qty +=instance.qty
                        multiple_size.save()  
                
            except Multiple_Size.DoesNotExist:
                
                multiple_size = Multiple_Size.objects.create(branch_product = branch_product,
                                             size = instance.size_instance)
                if action == "current_qty":
                    multiple_size.current_qty += instance.qty
                    multiple_size.save()
                elif action == "bad_qty":
                    multiple_size.bad_qty += instance.qty
                    multiple_size.current_qty -= instance.qty
                    multiple_size.save()
                elif action == "returned_qty":
                    multiple_size.returned_qty += instance.qty
                    multiple_size.current_qty +=instance.qty
                    multiple_size.save()
                
        except Branch_Product.DoesNotExist:
            branch_product = Branch_Product.objects.create(branch = instance.branch, 
                                            product = instance.product,
                                            current_qty = instance.qty,
                                            is_multiple_sized = True)
            multiple_size = Multiple_Size.objects.create(branch_product = branch_product,
                                             size = instance.size_instance)
            if action == "current_qty":
                multiple_size.current_qty += instance.qty
                multiple_size.save()
            elif action == "bad_qty":
                multiple_size.bad_qty += instance.qty
                multiple_size.current_qty -= instance.qtyiff
                multiple_size.save()
            elif action == "returned_qty":
                multiple_size.returned_qty += instance.qty
                multiple_size.current_qty +=instance.qty
                multiple_size.save()
    else:
         try: 
            branch_product =  Branch_Product.objects.get(branch = instance.branch,
                                                            product = instance.product,is_multiple_sized=False )
            if instance.pk:
                old_instance = model.objects.get(pk=instance.pk)
                diff = instance.qty - old_instance.qty
                if action == "current_qty":
                    branch_product.current_qty += diff
                    branch_product.save()
                elif action == "bad_qty":
                    branch_product.bad_qty += diff
                    branch_product.current_qty -= diff
                    branch_product.save()
                elif action == "returned_qty":
                    branch_product.returned_qty += diff
                    branch_product.current_qty +=diff  
                    branch_product.save()   
            else: 
                if action == "current_qty":
                    branch_product.current_qty += instance.qty
                    branch_product.save()
                elif action == "bad_qty":
                    branch_product.bad_qty += instance.qty
                    branch_product.current_qty -= instance.qty
                    branch_product.save()
                elif action == "returned_qty":
                    branch_product.returned_qty += instance.qty
                    branch_product.current_qty +=instance.qty  
                    branch_product.save()     
         except Branch_Product.DoesNotExist:
            branch_product =  Branch_Product.objects.create(branch = instance.branch, 
                                            product = instance.product)
            if action == "current_qty":
                branch_product.current_qty += instance.qty
                branch_product.save()
            elif action == "bad_qty":
                branch_product.bad_qty += instance.qty
                branch_product.current_qty -= instance.qty
                branch_product.save()
            elif action == "returned_qty":
                branch_product.returned_qty += instance.qty
                branch_product.current_qty +=instance.qty  
                branch_product.save()
                
                
def update_branch_Product_on_delete(instance,action):
    if instance.size_instance:
        try: 
            branch_product =  Branch_Product.objects.get(branch = instance.branch,
                                                            product = instance.product,is_multiple_sized=True )
            try:
                multiple_size = Multiple_Size.objects.get(branch_product = branch_product.id,
                                                     size = instance.size_instance)
                if action == "current_qty":
                    multiple_size.current_qty -= instance.qty
                    multiple_size.save() 
                elif action == "bad_qty":
                    multiple_size.current_qty += instance.qty
                    multiple_size.bad_qty -= instance.qty
                    multiple_size.save()
                elif action == "returned_qty":
                    multiple_size.current_qty -= instance.qty
                    multiple_size.returned_qty -= instance.qty
                    multiple_size.save()
            except Multiple_Size.DoesNotExist:
                pass      
        except Branch_Product.DoesNotExist:
            pass
    else:         
        try: 
            branch_product =  Branch_Product.objects.get(branch = instance.branch,
                                                            product = instance.product,is_multiple_sized=False )  
            if action == "current_qty":
                branch_product.current_qty -= instance.qty
                branch_product.save() 
            elif action == "bad_qty":
                branch_product.current_qty += instance.qty
                branch_product.bad_qty -= instance.qty
                branch_product.save()
            elif action == "returned_qty":
                branch_product.current_qty -= instance.qty
                branch_product.returned_qty -= instance.qty
                branch_product.save()  
        except Branch_Product.DoesNotExist:
            pass
       
