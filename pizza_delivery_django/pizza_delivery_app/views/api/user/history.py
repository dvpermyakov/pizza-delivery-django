from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pizza_delivery_app.models import User, Order

__author__ = 'Administrator'


@csrf_exempt
def order_history(request):
    user_id = request.GET.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponseBadRequest()
    orders = Order.objects.filter(user=user)
    return JsonResponse({
        'history': [order.dict() for order in orders]
    })