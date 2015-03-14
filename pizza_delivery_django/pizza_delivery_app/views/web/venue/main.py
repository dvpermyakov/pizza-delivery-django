from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def main_page(request, venue_id):
    return render(request, 'web/venue/main.html')