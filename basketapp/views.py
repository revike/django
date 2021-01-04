from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from basketapp.models import Basket
from mainapp.models import Product


@login_required
def basket(request):
    title = 'корзина'
    basket_items = Basket.objects.filter(
        user=request.user).order_by('product__category')
    content = {
        'title': title,
        'basket_items': basket_items
    }
    return render(request, 'basketapp/basket.html', content)


@login_required
def add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('mainapp:product', args=[pk]))
    product = get_object_or_404(Product, pk=pk)
    basket_item = Basket.objects.filter(
        user=request.user, product=product).first()

    if not basket_item:
        basket_item = Basket(user=request.user, product=product)

    basket_item.quantity += 1
    basket_item.save()

    # возвращаем на ту страницу, откуда пользователь пришел (request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# @login_required
# def delete(request, pk):
#     basket_item = get_object_or_404(Basket, pk=pk)
#     basket_item.delete()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_ajax(request, pk, quantity):
    if request.is_ajax():
        basket_for_delete = Basket.objects.get(pk=pk)
        basket_for_delete.quantity = quantity
        basket_for_delete.save()
        product_quantity = Product.objects.get(basket__user_id=request.user.id).quantity
        product_quantity += basket_for_delete.quantity
        basket_for_delete.save()
        basket_for_delete.delete()

    basket_items = Basket.objects.filter(
        user=request.user).order_by('product__category')

    content = {
        'basket_items': basket_items
    }

    result = render_to_string(
        'basketapp/includes/inc_basket_list.html', content)
    return JsonResponse({'result': result})


@login_required
def edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=pk)

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.quantity = quantity
            new_basket_item.save()
            new_basket_item.delete()

        basket_items = Basket.objects.filter(
            user=request.user).order_by('product__category')

        content = {
            'basket_items': basket_items
        }

        result = render_to_string(
            'basketapp/includes/inc_basket_list.html', content)
        return JsonResponse({'result': result})
