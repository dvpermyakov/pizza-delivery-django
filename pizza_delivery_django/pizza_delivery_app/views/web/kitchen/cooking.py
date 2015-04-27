from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from pizza_delivery_app.models import Cook, CookedProduct, VenueProduct
from pizza_delivery_app.models.order import OrderProduct

__author__ = 'dvpermyakov'


def cook_item(request):
    order_product_id = request.POST.get('order_product_id')
    try:
        order_product = OrderProduct.objects.get(id=order_product_id)
    except OrderProduct.DoesNotExist:
        return HttpResponseBadRequest()
    order_product.cook()
    return JsonResponse({
        'order_product_id': order_product.id,
        'status': order_product.status
    })


def cooking_list(request):
    cook = Cook.get_cook_by_username(request.user.username)
    cooked_products = [VenueProduct.objects.filter(venue=cook.venue, product=product) for product in CookedProduct.objects.filter(cook=cook)]
    items = OrderProduct.objects.filter(status=OrderProduct.NEW, venue_product__in=cooked_products)
    values = {
        'products': items
    }
    return render(request, 'web/kitchen/product_list.html', values)