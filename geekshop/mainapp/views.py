import json
import os

from django.conf import settings
from django.shortcuts import render

from mainapp.models import Product, ProductCategory

# Create your views here.


def main(request):
    title = 'главная'
    products = Product.objects.all()[:4]
    content = {
        'title': title,
        'products': products,
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    title = 'продукты'
    links_menu = ProductCategory.objects.all()
    content = {
        'title': title,
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', content)


def contacts(request):
    title = 'контакты'
    file = os.path.join(settings.BASE_DIR,
                        'mainapp/json/contact__locations.json')
    with open(file, encoding='utf-8') as obj:
        address = json.load(obj)

    content = {
        'title': title,
        'address': address,
    }
    return render(request, 'mainapp/contact.html', content)
