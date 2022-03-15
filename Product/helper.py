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
     