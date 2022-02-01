
from Branch.models import Branch
from Product.models import Category


def context_processor(request):
    branches = Branch.objects.all()
    categories = Category.objects.all()
    return {"branches": branches, "categories":categories}