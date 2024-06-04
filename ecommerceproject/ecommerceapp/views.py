from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from . models import Category,Product
from django.core.paginator import Paginator, EmptyPage, InvalidPage

# Create your views here.
# def index(request):
#     return HttpResponse("hi i am ecommerceapp")

from django.http import Http404


def allProdCat(request, c_slug=None):
    c_page = None
    products_list = None

    if c_slug is not None:
        try:
            c_page = Category.objects.get(slug=c_slug)
            products_list = Product.objects.filter(category=c_page, available=True)
        except Category.DoesNotExist:
            raise Http404("Category does not exist")
    else:
        products_list = Product.objects.filter(available=True)

    paginator = Paginator(products_list, 6)

    page = request.GET.get('page', 1)
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)

    return render(request, "category.html", {'category': c_page, 'products': products})


def proDetail(request,c_slug,product_slug):
    try:
        product=Product.objects.get(category__slug=c_slug,slug=product_slug)
    except Exception as e:
        raise e
    return render(request,'product.html',{'product':product})