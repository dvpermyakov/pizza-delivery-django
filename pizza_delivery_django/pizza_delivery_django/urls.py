from django.conf.urls import patterns, url
from pizza_delivery_app.views import api, web
from pizza_delivery_app.views.web import company, venue
from pizza_delivery_app.views.first_page import first_page

urlpatterns = patterns('',
    url(r'^$', first_page),

    url(r'^api/menu/$', api.menu),

    url(r'^web/login/$', web.login),
    url(r'^web/logout/$', web.logout),
    url(r'^web/main/$', web.main_page),

    url(r'^web/company/signup/$', company.signup),
    url(r'^web/company/main/$', company.main_page),

    url(r'^web/venue/signup/$', venue.signup),
    url(r'^web/venue/map/$', venue.map_venues),
    url(r'^web/(?P<venue_id>\d+)/venue/main/$', venue.main_page),

    url(r'^web/(?P<venue_id>\d+)/menu/$', web.menu),
    url(r'^web/(?P<venue_id>\d+)/menu/(?P<category_id>\d+)/category/$', web.category),
    url(r'^web/(?P<venue_id>\d+)/menu/(?P<category_id>\d+)/category/create/$', web.create_category),
    url(r'^web/(?P<venue_id>\d+)/menu/(?P<category_id>\d+)/category/change/$', web.change_category),
    url(r'^web/(?P<venue_id>\d+)/menu/(?P<category_id>\d+)/category/delete/$', web.delete_category),

    url(r'^web/(?P<venue_id>\d+)/menu/(?P<category_id>\d+)/product/create/$', web.create_product),
    url(r'^web/(?P<venue_id>\d+)/menu/(?P<product_id>\d+)/product/change/$', web.change_product),
    url(r'^web/(?P<venue_id>\d+)/menu/(?P<product_id>\d+)/product/delete/$', web.delete_product),
    url(r'^web/(?P<venue_id>\d+)/menu/(?P<venue_product_id>\d+)/product/change/status/$', web.change_status),

    url(r'^web/(?P<venue_id>\d+)/menu/modifiers$', web.modifiers),
    url(r'^web/(?P<venue_id>\d+)/menu/active_modifiers$', web.modifiers),
    url(r'^web/(?P<venue_id>\d+)/menu/modifiers/single_modifiers/create$', web.create_single_modifier),
)