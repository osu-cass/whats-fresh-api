from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^stories/(?P<id>\d+)/?$', 
        'whats_fresh_api.views.story.story_details', 
        name='story-details'),

    url(r'^products/?$', 
        'whats_fresh_api.views.product.product_list', 
        name='products-list'),
    url(r'^products/(?P<id>\d+)/?$', 
        'whats_fresh_api.views.product.product_details', 
        name='product-details'),
    url(r'^products/vendors/(?P<id>\d+)/?$',
        'whats_fresh_api.views.product.product_vendor',
        name='product-vendor'),

    url(r'^vendors/?$', 
        'whats_fresh_api.views.vendor.vendor_list', 
        name='vendors-list'), 
    url(r'^vendors/(?P<id>\d+)/?$', 
        'whats_fresh_api.views.vendor.vendor_details', 
        name='vendor-details'),
    url(r'^vendors/products/(?P<id>\d+)/?$', 
        'whats_fresh_api.views.vendor.vendors_products', 
        name='vendors-products'),

    url(r'^preparations/(?P<id>\d+)/?$', 
        'whats_fresh_api.views.preparation.preparation_details', 
        name='preparation-details'),

    url(r'^entry/vendors/new/?$', 
        'whats_fresh_api.views.data_entry.vendors.vendor', 
        name='new-vendor'),

    url(r'^entry/vendors/(?P<id>\d+)/?$', 
        'whats_fresh_api.views.data_entry.vendors.vendor', 
        name='edit-vendor'),

    url(r'^entry/vendors/?$', 
        'whats_fresh_api.views.data_entry.vendors.vendor_list', 
        name='list-vendors-edit'),

    url(r'^entry/products/(?P<id>\d+)/?$', 
        'whats_fresh_api.views.data_entry.products.product', 
        name='edit-product'),

    url(r'^entry/products/new/?$', 
        'whats_fresh_api.views.data_entry.products.product', 
        name='new-product'),

    url(r'^entry/products/?$',
        'whats_fresh_api.views.data_entry.products.product_list', 
        name='entry-list-products'),

    url(r'^entry/preparations/new/?$', 
        'whats_fresh_api.views.data_entry.preparations.preparation', 
        name='new-preparation'),

    url(r'^entry/preparations/(?P<id>\d+)/?$', 
        'whats_fresh_api.views.data_entry.preparations.preparation', 
        name='edit-preparation'),

    url(r'^entry/preparations/?$', 
        'whats_fresh_api.views.data_entry.preparations.preparation_list', 
        name='entry-list-preparations'),

    url(r'^login/?$', 
        'whats_fresh_api.views.data_entry.login.login_user', 
        name='login'),
)
