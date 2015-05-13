from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from pizza_delivery_app.methods.times import timestamp
from pizza_delivery_app.models import Cook, CookedOrderedProduct

__author__ = 'dvpermyakov'


@login_required
@permission_required('pizza_delivery_app.cook')
def cook_item(request):
    product_id = request.POST.get('product_id')
    try:
        product = CookedOrderedProduct.objects.get(id=product_id)
    except CookedOrderedProduct.DoesNotExist:
        return HttpResponseBadRequest()
    old_status = product.status
    product.set_cooked()
    product.product.cook()
    return JsonResponse({
        'id': product.id,
        'number': product.product.id,
        'status_name': CookedOrderedProduct.STATUS_CHOICES[product.status][1],
        'status': product.status,
        'old_status': old_status
    })


def _prepare_products(products):
    last_time = 0
    for product in products:
        if timestamp(product.created) > last_time:
            last_time = timestamp(product.created)
        product.name = product.product.venue_product.product.name
        product.status_name = CookedOrderedProduct.STATUS_CHOICES[product.status][1]
        product.number = product.product.id
    return products, last_time


@login_required
@permission_required('pizza_delivery_app.cook')
def cooking_list(request):
    cook = Cook.get_cook_by_username(request.user.username)
    today = datetime.utcnow().replace(hour=0, minute=0, second=0)
    products = CookedOrderedProduct.objects.filter(cook=cook, created__gte=today)
    products, last_time = _prepare_products(products)
    values = {
        'products': products,
        'last_time': last_time + 1
    }
    return render(request, 'web/kitchen/product_list.html', values)


@login_required
@permission_required('pizza_delivery_app.cook')
def new_products(request):
    cook = Cook.get_cook_by_username(request.user.username)
    last_time = request.GET.get('last_time')
    today = datetime.utcnow().replace(hour=0, minute=0, second=0)
    if timestamp(today) > int(last_time):
        last_time = timestamp(today)
    if last_time:
        last_time = datetime.utcfromtimestamp(int(last_time))
        products = CookedOrderedProduct.objects.filter(created__gt=last_time, cook=cook)
        if products:
            products, last_time = _prepare_products(products)
            product_dicts = [product.dict() for product in products]
        else:
            product_dicts = []
            last_time = timestamp(last_time)
        return JsonResponse({
            'products': product_dicts,
            'last_time': last_time if not product_dicts else last_time + 1
        })
    else:
        return HttpResponseBadRequest()