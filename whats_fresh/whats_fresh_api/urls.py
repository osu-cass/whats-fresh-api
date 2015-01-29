from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns(
    '',
    url(r'^1/stories/?$',
        'whats_fresh.whats_fresh_api.views.story.story_list',
        name='stories-list'),
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
        'whats_fresh.whats_fresh_api.views.entry.vendors.vendor',
        name='new-vendor'),

    url(r'^entry/vendors/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.entry.vendors.vendor',
        name='edit-vendor'),

    url(r'^entry/vendors/?$',
        'whats_fresh.whats_fresh_api.views.entry.vendors.vendor_list',
        name='list-vendors-edit'),

    url(r'^entry/products/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.entry.products.product',
        name='edit-product'),

    url(r'^entry/products/new/?$',
        'whats_fresh.whats_fresh_api.views.entry.products.product',
        name='new-product'),

    url(r'^entry/products/?$',
        'whats_fresh.whats_fresh_api.views.entry.products.product_list',
        name='entry-list-products'),

    url(r'^entry/stories/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.entry.stories.story',
        name='edit-story'),

    url(r'^entry/stories/new/?$',
        'whats_fresh.whats_fresh_api.views.entry.stories.story',
        name='new-story'),

    url(r'^entry/stories/?$',
        'whats_fresh.whats_fresh_api.views.entry.stories.story_list',
        name='entry-list-stories'),

    url(r'^entry/preparations/new/?$',
        'whats_fresh.whats_fresh_api.views.entry.preparations.preparation',
        name='new-preparation'),

    url(r'^entry/preparations/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.entry.preparations.preparation',
        name='edit-preparation'),

    url(r'^entry/preparations/?$',
        'whats_fresh.whats_fresh_api.views.entry.preparations.prep_list',
        name='entry-list-preparations'),

    url(r'^entry/images/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.entry.images.image',
        name='edit-image'),

    url(r'^entry/images/?$',
        'whats_fresh.whats_fresh_api.views.entry.images.image_list',
        name='entry-list-images'),

    url(r'^entry/images/new/?$',
        'whats_fresh.whats_fresh_api.views.entry.images.image',
        name='new-image'),

    url(r'^entry/videos/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.entry.videos.video',
        name='edit-video'),

    url(r'^entry/videos/?$',
        'whats_fresh.whats_fresh_api.views.entry.videos.video_list',
        name='entry-list-videos'),

    url(r'^entry/videos/new/?$',
        'whats_fresh.whats_fresh_api.views.entry.videos.video',
        name='new-video'),

    url(r'^login/?$',
        'whats_fresh.whats_fresh_api.views.entry.login.login_user',
        name='login'),

    url(r'^logout/?$',
        'whats_fresh.whats_fresh_api.views.entry.login.logout_user',
        name='logout'),

    url(r'^/?$',
        'whats_fresh.whats_fresh_api.views.entry.login.root',
        name='root'),

    url(r'^entry/?$',
        'whats_fresh.whats_fresh_api.views.entry.home.home',
        name='home'),

)
