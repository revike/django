import json
import os
import random

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from basketapp.models import Basket
from mainapp.models import Product, ProductCategory

# Create your views here.


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return []


def get_hot_product():
    products_list = Product.objects.all()
    return random.sample(list(products_list), 1)[0]


def get_same_products(hot_product):
    return Product.objects.filter(category__pk=hot_product.category.pk).exclude(pk=hot_product.pk)[:3]


def main(request):
    title = 'главная'
    products = Product.objects.all()[:4]

    content = {
        'title': title,
        'products': products,
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None, page=1):
    title = 'продукты'
    links_menu = ProductCategory.objects.all()

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

        paginator = Paginator(products_list, 2)
        try:
            product_paginator = paginator.page(page)
        except PageNotAnInteger:
            product_paginator = paginator.page(1)
        except EmptyPage:
            product_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'links_menu': links_menu,
            'products': product_paginator,
            'category': category,
            'basket': get_basket(request.user)
        }

        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
        'basket': get_basket(request.user),
        'hot_product': hot_product,
    }
    return render(request, 'mainapp/products.html', content)


def product(requests, pk):
    title = 'продукты'
    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(requests.user)
    }
    return render(requests, 'mainapp/product.html', content)


def contacts(request):
    title = 'контакты'
    file = os.path.join(settings.BASE_DIR,
                        'mainapp/json/contact__locations.json')
    with open(file, encoding='utf-8') as obj:
        address = json.load(obj)

    content = {
        'title': title,
        'address': address,
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/contact.html', content)


def error_404(request, exception):
    # Выборка из базы, преобразование данных и т.п.
    return render(request, '404.html', {'item': 'Своя страница 404'}, status=404)
