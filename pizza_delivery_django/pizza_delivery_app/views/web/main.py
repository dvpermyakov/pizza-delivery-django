__author__ = 'dvpermyakov'

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from pizza_delivery_app.permissions.groups import CHIEF_GROUP, MANAGER_GROUP, COOK_GROUP
from django.http import HttpResponseForbidden


@login_required
def main_page(request):
    user_groups = request.user.groups.all()
    if CHIEF_GROUP in user_groups:
        return redirect('/web/company/main')
    elif MANAGER_GROUP in user_groups:
        return redirect('/web/venue/orders/list/')
    elif COOK_GROUP in user_groups:
        return redirect('/web/kitchen/products/list/')
    else:
        return HttpResponseForbidden()