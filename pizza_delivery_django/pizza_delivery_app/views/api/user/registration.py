from django.http import JsonResponse
from pizza_delivery_app.models.user import User
from django.views.decorators.csrf import csrf_exempt

__author__ = 'dvpermyakov'


@csrf_exempt
def create_or_update(request):
    user_id = request.POST.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        user = None
    name = request.POST.get('name')
    if user:
        user.name = name
    else:
        user = User(name=name)
    user.save()
    return JsonResponse(user.dict())