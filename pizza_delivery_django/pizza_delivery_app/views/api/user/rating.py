import json
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pizza_delivery_app.models import User, Rating, Product, Address, Venue, Order

__author__ = 'dvpermyakov'


@csrf_exempt
def set_rating(request):
    user_id = request.POST.get('user_id')
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
        try:
            rating_obj = Rating.objects.get(user=user, product=product)
            if rating_obj.rating != float(rating.get('rating')):
                rating_obj.rating = float(rating.get('rating'))
                rating_obj.save()
        except Rating.DoesNotExist:
            Rating(user=user, product=product, rating=float(rating.get('rating'))).save()
    return JsonResponse({
        'success': True
    })


MAX_PREFERENCES = 5


@csrf_exempt
def get_preferences(request):  # collaborative filtering, slope one
    user_id = request.POST.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponseBadRequest()
    lat = request.POST.get('lat')
    lon = request.POST.get('lon')
    if not lat or not lon:
        return HttpResponseBadRequest()
    lat = float(lat)
    lon = float(lon)
    address = Address(lat=lat, lon=lon)
    venues = Venue.objects.all()
    suited_venues = []
    suited_categories = []
    for venue in venues:
        if venue not in suited_venues and venue.is_included(address) and venue.first_category not in suited_categories:
            suited_venues.append(venue)
            suited_categories.append(venue.first_category)
    products = []
    for venue in suited_venues:
        products.extend(venue.get_products_from_menu(venue_product=False))
    orders = Order.objects.filter(user=user, status=Order.CLOSED)
    for order in orders:
        for product in order.get_products():
            product = product.venue_product.product
            if product in products:
                products.remove(product)
    ratings = Rating.objects.filter(user=user)
    results = []
    for product in products:
        sum = 0
        amount = 0
        for rate in ratings:
            other_users = User.objects.filter(rating__product=rate.product).filter(rating__product=product)
            differ = 0
            for other_user in other_users:
                differ += Rating.objects.get(user=other_user, product=rate.product).rating - \
                          Rating.objects.get(user=other_user, product=product).rating
            sum += (rate.rating + differ) * len(other_users)
            amount += len(other_users)
        results.append({
            'product_id': product.id,
            'rating': sum / amount if amount else 0.0
        })
    if len(results) > MAX_PREFERENCES:
        remain_results = []
        for i in xrange(MAX_PREFERENCES):
            index = 0
            for i, result in enumerate(results):
                if result['rating'] > results[index]['rating']:
                    index = i
            remain_results.append(results[index])
            results.remove(results[index])
    else:
        remain_results = results
    return JsonResponse({
        'ratings': remain_results
    })