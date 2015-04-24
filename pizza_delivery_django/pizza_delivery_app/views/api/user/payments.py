from django.http import HttpResponseBadRequest, JsonResponse
from pizza_delivery_app.models import User
from pizza_delivery_app.models.user import YdWallet

__author__ = 'Administrator'


def available_payment_types(request):
    user_id = request.GET.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponseBadRequest()
    return JsonResponse({
        'yd': [yandex_wallet.dict() for yandex_wallet in YdWallet.objects.filter(user=user)]
    })