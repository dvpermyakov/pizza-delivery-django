from django.conf.urls import patterns, url
from pizza_delivery_app.views import api, web
from pizza_delivery_app.views.web import company, venue, kitchen
from pizza_delivery_app.views.first_page import first_page
from pizza_delivery_app.views.api import user

urlpatterns = patterns('',
    url(r'^$', first_page),

    url(r'^api/yandex_money/auth/$', user.auth),
    url(r'^api/yandex_money/get_balance/$', user.get_balance),
    url(r'^api/user/card/success/$', user.set_token),  # callback after filling data in yd

    url(r'^api/user/create_or_update/$', user.create_or_update),
    url(r'^api/user/payments/avail/$', user.available_payment_types),
    url(r'^api/user/history/$', user.order_history),
    url(r'^api/user/ratings/$', user.set_rating),

    url(r'^api/address/get_home/by_coordinates/$', api.get_home_by_coordinates),
    url(r'^api/address/get_coordinates/by_home/$', api.get_coordinates_by_home),
    url(r'^api/address/get_address/by_string/$', api.autocomplete_address),

    url(r'^api/order/$', api.order),
    url(r'^api/check_order/$', api.check_order),

    url(r'^api/menu/$', api.menu),
    url(r'^api/menu/item_info/$', api.menu_item_info),
    url(r'^api/menu/last_modified/$', api.last_modified_menu),
    url(r'^api/companies/$', api.companies),
    url(r'^api/venues/$', api.venues),

    url(r'^tmp/rate/$', venue.set_ratings),  # todo: remove it

    url(r'^web/login/$', web.login),
    url(r'^web/logout/$', web.logout),
    url(r'^web/main/$', web.main_page),

    url(r'^web/kitchen/signup/$', kitchen.signup),
    url(r'^web/kitchen/products/list/$', kitchen.cooking_list),
    url(r'^web/kitchen/products/cook/$', kitchen.cook_item),
    url(r'^web/kitchen/products/new/$', kitchen.new_products),

    url(r'^web/company/signup/$', company.signup),
    url(r'^web/company/main/$', company.main_page),

    url(r'^web/venue/signup/$', venue.signup),
    url(r'^web/venue/map/$', venue.map_venues),
    url(r'^web/venue/restriction_map/$', venue.restriction_map),
    url(r'^web/(?P<venue_id>\d+)/venue/main/$', venue.main_page),
    url(r'^web/venue/orders/confirm/$', venue.confirm_order),
    url(r'^web/venue/orders/deliver/$', venue.deliver_order),
    url(r'^web/venue/orders/close/$', venue.close_order),
    url(r'^web/venue/orders/list/$', venue.order_list),
    url(r'^web/venue/orders/new/$', venue.new_orders),
    url(r'^web/venue/orders/update/$', venue.update_statuses),
    url(r'^web/venue/cooks/list/$', venue.cooks_list),

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