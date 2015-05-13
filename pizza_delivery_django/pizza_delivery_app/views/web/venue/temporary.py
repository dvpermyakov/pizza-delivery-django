from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pizza_delivery_app.models import Venue, User, Rating, Product
import random

__author__ = 'dvpermyakov'


@csrf_exempt
def set_ratings(request):
    venue_id = request.POST.get('venue_id')
    venue = Venue.objects.get(id=venue_id)
    products = venue.get_products_from_menu(venue_product=False)
    ids = [product.id for product in products]
    rs = []
    for i in range(2):
        user = User()
        user.save()
        for j in range(len(ids)):
            product_id = ids[random.randint(0, len(ids) - 1)]
            product = Product.objects.get(id=product_id)
            ratings = Rating.objects.filter(user=user, product=product)
            if ratings:
                continue
            rating = random.randint(1, 5)
            r = Rating(user=user, rating=rating, product=product)
            r.save()
            rs.append(r)
    return JsonResponse({
        'ratings': [r.dict() for r in rs]
    })


def get_specific_user(request):
    product1 = Product.objects.get(id=1)
    product2 = Product.objects.get(id=2)
    users = User.objects.filter(rating__product=product1).filter(rating__product=product2)
    return JsonResponse({
        'users': [user.dict() for user in users]
    })