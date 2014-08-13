from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^stories/(?P<id>\d+)/?$',
        'whats_fresh_api.views.story.story_details', name='story-details'),

    url(r'^products/?$', 'whats_fresh_api.views.product.product_list',
        name='products-list'),
    url(r'^products/(?P<id>\d+)/?$',
        'whats_fresh_api.views.product.product_details',
        name='product-details'),

    url(r'^vendors/?$', 'whats_fresh_api.views.vendor.vendor_list',
        name='vendors-list'),
    url(r'^vendors/products/(?P<id>\d+)/?$',
        'whats_fresh_api.views.vendor.vendors_products',
        name='vendors-products'),
)

