from django.http import JsonResponse
from pizza_delivery_app.models import Company

__author__ = 'dvpermyakov'


def companies(request):
    return JsonResponse({
        'companies': [company.dict() for company in Company.objects.all()]
    })