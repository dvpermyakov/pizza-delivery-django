import logging
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pizza_delivery_app.models import Cook, CookedOrderedProduct

__author__ = 'dvpermyakov'


@csrf_exempt  # todo: delete it
def cook_item(request):
    product_id = request.POST.get('product_id')
    try:
        product = CookedOrderedProduct.objects.get(id=product_id)
    except CookedOrderedProduct.DoesNotExist:
        return HttpResponseBadRequest()
    product.set_cooked()
    product.product.cook()
    return JsonResponse({
        'product_id': product_id,
        'status': product.status
    })


def cooking_list(request):
    cook = Cook.get_cook_by_username(request.user.username)
    products = CookedOrderedProduct.objects.filter(cook=cook)
    for product in products:
        product.name = product.product.venue_product.product.name
    values = {
        'products': products
    }
    return render(request, 'web/kitchen/product_list.html', values)