import json
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pizza_delivery_app.models import User, Rating, Product

__author__ = 'dvpermyakov'


@csrf_exempt
def set_rating(request):
    user_id = request.GET.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponseBadRequest()
    try:
        rating_data = json.loads(request.POST.get('rating_data'))
    except ValueError:
        return HttpResponseBadRequest()
    for rating in rating_data.get('ratings', []):
        try:
            product = Product.objects.get(id=rating.get('product_id'))
        except Product.DoesNotExist:
            return HttpResponseBadRequest()
        rating_obj = Rating.objects.get(user=user, product=product)
        if rating_obj.rating != float(rating.get('rating')):
            rating_obj.rating = float(rating.get('rating'))
            rating_obj.save()
    return JsonResponse({
        'success': True
    })