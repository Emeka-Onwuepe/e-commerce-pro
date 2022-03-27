
from Branch.models import Branch
from Product.models import Category


def context_processor(request):
    branches = Branch.objects.all()
    categories = Category.objects.all()
    unsorted_categories = Category.objects.filter(category__product_type__publish = True)
    sorted_categories = []
    for category in unsorted_categories:
        if category not in sorted_categories:
            sorted_categories.append(category)
    return {"branches": branches, "categories":categories,
            "sorted_categories":sorted_categories}