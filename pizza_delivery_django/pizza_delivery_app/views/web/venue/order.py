from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pizza_delivery_app.models import Order

__author__ = 'Administrator'


@csrf_exempt  # TODO: remove it!
def confirm_order(request):
    order_id = request.POST.get('order_id')
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponseBadRequest()
    order.confirm()
    return JsonResponse({
        'success': True
    })