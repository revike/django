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
    links_menu = ProductCategory.objects.all()
    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', content)


def contacts(request):
    file = os.path.join(settings.BASE_DIR, 'address.json')
    with open(file) as obj:
        address = json.load(obj)
        
    content = {
        'title': 'Контакты',
        'address': address,
    }
    return render(request, 'mainapp/contact.html', content)
