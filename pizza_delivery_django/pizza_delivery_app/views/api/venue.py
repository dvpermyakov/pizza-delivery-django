from django.http import JsonResponse, HttpResponseBadRequest
from pizza_delivery_app.models import Venue, Company

__author__ = 'dvpermyakov'


def venues(request):
    company_id = request.GET.get('company_id')
    if company_id:
        company = Company.objects.get(id=company_id)
        try:
            return JsonResponse({
                'venues': [venue.dict() for venue in Venue.objects.filter(company=company)]
            })
        except Company.DoesNotExist:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()