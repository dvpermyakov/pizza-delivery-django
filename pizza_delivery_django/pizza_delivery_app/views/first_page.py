from django.shortcuts import redirect


def first_page(request):
    return redirect('/web/main')