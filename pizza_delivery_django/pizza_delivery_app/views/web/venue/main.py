from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render


@login_required
@permission_required('pizza_delivery_app.crud_orders')
def main_page(request, venue_id):
    return render(request, 'web/venue/main.html')