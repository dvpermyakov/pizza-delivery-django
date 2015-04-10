from django.conf.urls import patterns, url
from pizza_delivery_app.views import api, web
from pizza_delivery_app.views.web import company, venue
from pizza_delivery_app.views.first_page import first_page

urlpatterns = patterns('',
    url(r'^$', first_page),

    url(r'^api/menu/$', api.menu),
    url(r'^api/companies/$', api.companies),

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
    url(r'^web/(?P<venue_id>\d+)/menu/category/delete/$', web.delete_category),

    url(r'^web/(?P<venue_id>\d+)/menu/(?P<category_id>\d+)/product/create/$', web.create_product),
    url(r'^web/(?P<venue_id>\d+)/menu/(?P<product_id>\d+)/product/change/$', web.change_product),
    url(r'^web/(?P<venue_id>\d+)/menu/product/delete/$', web.delete_product),

    url(r'^web/(?P<venue_id>\d+)/menu/product/change/status/$', web.change_status),
    url(r'^web/(?P<venue_id>\d+)/menu/product/change/price/$', web.change_price),

    url(r'^web/(?P<venue_id>\d+)/menu/modifiers/$', web.modifiers),
    #url(r'^web/(?P<venue_id>\d+)/menu/active_modifiers/$', web.modifiers),
    url(r'^web/(?P<venue_id>\d+)/menu/modifiers/single_modifiers/create/$', web.create_single_modifier),
    url(r'^web/(?P<venue_id>\d+)/menu/modifiers/(?P<modifier_id>\d+)/single_modifier/change/$', web.change_single_modifier),
    url(r'^web/(?P<venue_id>\d+)/menu/modifiers/(?P<modifier_id>\d+)/single_modifier/select_products/$', web.select_products_for_single_modifier),
    #url(r'^web/(?P<venue_id>\d+)/menu/modifiers/single_modifiers/delete/$', ),

    url(r'^web/(?P<venue_id>\d+)/menu/modifiers/group_modifiers/create/$', web.create_group_modifier),
    url(r'^web/(?P<venue_id>\d+)/menu/modifiers/(?P<modifier_id>\d+)/group_modifier/change/$', web.change_group_modifier),
    #url(r'^web/(?P<venue_id>\d+)/menu/modifiers/group_modifiers/delete/$', ),
    url(r'^web/(?P<venue_id>\d+)/menu/modifiers/group_modifier_items/create/$', web.create_group_modifier_item),
    url(r'^web/(?P<venue_id>\d+)/menu/modifiers/(?P<modifier_id>\d+)/group_modifiers/change$', web.change_group_modifier),
    url(r'^web/(?P<venue_id>\d+)/menu/modifiers/(?P<modifier_id>\d+)/group_modifier/select_products/$', web.select_products_for_group_modifier),
)