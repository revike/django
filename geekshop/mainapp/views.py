import json
import os

from django.conf import settings
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory

# Create your views here.


def main(request):
    title = 'главная'
    products = Product.objects.all()[:4]
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    content = {
        'title': title,
        'products': products,
        'basket': basket
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    title = 'продукты'
    links_menu = ProductCategory.objects.all()

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category = {
                'name': 'все',
                'pk': 0
            }
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk)

        content = {
            'title': title,
            'links_menu': links_menu,
            'products': products_list,
            'category': category,
            'basket': basket
        }

        return render(request, 'mainapp/products_list.html', content)

    same_products = Product.objects.all()[3:5]
    content = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
        'basket': basket
    }
    return render(request, 'mainapp/products.html', content)


def contacts(request):
    title = 'контакты'
    file = os.path.join(settings.BASE_DIR,
                        'mainapp/json/contact__locations.json')
    with open(file, encoding='utf-8') as obj:
        address = json.load(obj)

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    content = {
        'title': title,
        'address': address,
        'basket': basket
    }
    return render(request, 'mainapp/contact.html', content)
