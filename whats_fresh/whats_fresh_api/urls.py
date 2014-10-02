from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^1/stories/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.story.story_details',
        name='story-details'),

    url(r'^1/products/?$',
        'whats_fresh.whats_fresh_api.views.product.product_list',
        name='products-list'),
    url(r'^1/products/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.product.product_details',
        name='product-details'),
    url(r'^1/products/vendors/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.product.product_vendor',
        name='product-vendor'),

    url(r'^1/vendors/?$',
        'whats_fresh.whats_fresh_api.views.vendor.vendor_list',
        name='vendors-list'),
    url(r'^1/vendors/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.vendor.vendor_details',
        name='vendor-details'),
    url(r'^1/vendors/products/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.vendor.vendors_products',
        name='vendors-products'),

    url(r'^1/preparations/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.preparation.preparation_details',
        name='preparation-details'),

    url(r'^1/locations/?$',
        'whats_fresh.whats_fresh_api.views.location.locations',
        name='locations'),

    url(r'^entry/vendors/new/?$',
        'whats_fresh.whats_fresh_api.views.data_entry.vendors.vendor',
        name='new-vendor'),

    url(r'^entry/vendors/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.data_entry.vendors.vendor',
        name='edit-vendor'),

    url(r'^entry/vendors/(?P<id>\d+)/delete/?$',
        'whats_fresh_api.views.data_entry.vendors.delete_vendor',
        name='delete-vendor'),

    url(r'^entry/vendors/?$',
        'whats_fresh.whats_fresh_api.views.data_entry.vendors.vendor_list',
        name='list-vendors-edit'),

    url(r'^entry/products/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.data_entry.products.product',
        name='edit-product'),

    url(r'^entry/products/(?P<id>\d+)/delete/?$',
        'whats_fresh_api.views.data_entry.products.delete_product',
        name='delete-product'),

    url(r'^entry/products/new/?$',
        'whats_fresh.whats_fresh_api.views.data_entry.products.product',
        name='new-product'),

    url(r'^entry/products/?$',
        'whats_fresh.whats_fresh_api.views.data_entry.products.product_list',
        name='entry-list-products'),

    url(r'^entry/preparations/new/?$',
        'whats_fresh.whats_fresh_api.views.data_entry.preparations.preparation',
        name='new-preparation'),

    url(r'^entry/preparations/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.data_entry.preparations.preparation',
        name='edit-preparation'),

    url(r'^entry/preparations/(?P<id>\d+)/delete/?$',
        'whats_fresh_api.views.data_entry.preparations.delete_preparation',
        name='delete-preparation'),

    url(r'^entry/preparations/?$',
        'whats_fresh.whats_fresh_api.views.data_entry.preparations.preparation_list',
        name='entry-list-preparations'),

    url(r'^login/?$',
        'whats_fresh.whats_fresh_api.views.data_entry.login.login_user',
        name='login'),

    url(r'^/?$',
        'whats_fresh.whats_fresh_api.views.data_entry.login.root',
        name='root'),

    url(r'^entry/?$',
        'whats_fresh.whats_fresh_api.views.data_entry.home.home',
        name='home'),

)
