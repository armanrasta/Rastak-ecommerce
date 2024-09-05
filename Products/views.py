from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from forms import SearchForm
from django.db.models import Q
# Create your views here.



def products_by_category(request):
    category = get_object_or_404(Category)
    products = Product.objects.filter(category=category)
    
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