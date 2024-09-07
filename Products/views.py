from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from .forms import SearchForm
from django.db.models import Q
# Create your views here.


def products_by_category(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'Products/products_by_category.html', context)

def category_list(request):
    categories = Category.objects.filter(is_subcat=False)
    context = {
        'categories': categories
    }
    return render(request, 'Products/category_list.html', context)


def product_detail(request, product_name):
    product = get_object_or_404(Product, name=product_name)
    pictures = product.pictures.all()
    colors = product.productcolor_set.all()
    context = {
        'product': product,
        'pictures': pictures,
        'colors': colors
    }
    return render(request, 'Products/product_detail.html', context)


def search(request):
    form = SearchForm()
    results = []
    
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Product.objects.filter(Q(name__icontains=query) | Q(brand__icontains=query)).distinct()
            
            return render(request, 'search.html',
                          {'form':form, 'results':results})
            
            
def home(request):
    
    return render(request, 'Products/home.html')