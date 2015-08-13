from django.conf.urls import patterns
from django.conf.urls import url
from whats_fresh.whats_fresh_api.templatetags import get_fieldname
from django.contrib import admin


urlpatterns = patterns(
    '',
    url(r'^1/'+get_fieldname.get_fieldname('stories_slug')+'/?$',
        'whats_fresh.whats_fresh_api.views.story.story_list',
        name='stories-list'),
    url(r'^1/'+get_fieldname.get_fieldname('stories_slug')+'/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.story.story_details',
        name='story-details'),

    url(r'^1/'+get_fieldname.get_fieldname('products_slug')+'/?$',
        'whats_fresh.whats_fresh_api.views.product.product_list',
        name='products-list'),
    url(r'^1/'+get_fieldname.get_fieldname('products_slug')+'/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.product.product_details',
        name='product-details'),
    url(r'^1/'+get_fieldname.get_fieldname('products_slug')+'/'
         + get_fieldname.get_fieldname('vendors_slug')+'/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.product.product_vendor',
        name='product-vendor'),

    url(r'^1/'+get_fieldname.get_fieldname('vendors_slug')+'/?$',
        'whats_fresh.whats_fresh_api.views.vendor.vendor_list',
        name='vendors-list'),
    url(r'^1/'+get_fieldname.get_fieldname('vendors_slug')+'/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.vendor.vendor_details',
        name='vendor-details'),
    url(r'^1/'+get_fieldname.get_fieldname('vendors_slug')+'/'
        + get_fieldname.get_fieldname('products_slug')+'/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.vendor.vendors_products',
        name='vendors-products'),

    url(r'^1/'+get_fieldname.get_fieldname('preparations_slug')
        + '/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.preparation.preparation_details',
        name='preparation-details'),

    url(r'^1/locations/?$',
        'whats_fresh.whats_fresh_api.views.location.locations',
        name='locations'),

    url(r'^entry/'+get_fieldname.get_fieldname('vendors_slug')+'/new/?$',
        'whats_fresh.whats_fresh_api.views.entry.vendors.vendor',
        name='new-vendor'),

    url(r'^entry/'+get_fieldname.get_fieldname('vendors_slug')
        + '/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.entry.vendors.vendor',
        name='edit-vendor'),

    url(r'^entry/'+get_fieldname.get_fieldname('vendors_slug')+'/?$',
        'whats_fresh.whats_fresh_api.views.entry.vendors.vendor_list',
        name='list-vendors-edit'),

    url(r'^entry/'+get_fieldname.get_fieldname('products_slug')
        + '/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.entry.products.product',
        name='edit-product'),

    url(r'^entry/'+get_fieldname.get_fieldname('products_slug')+'/new/?$',
        'whats_fresh.whats_fresh_api.views.entry.products.product',
        name='new-product'),

    # Endpoint for popup form in product.html
    url(r'^entry/'+get_fieldname.get_fieldname('products_slug')+'/new/'
        + get_fieldname.get_fieldname('preparations_slug')+'/new/?$',
        'whats_fresh.whats_fresh_api.views.entry.preparations.preparation_ajax',  # noqa
        name='preparation_ajax'),

    # Endpoint for popup form in vendor.html
    url(r'^entry/'+get_fieldname.get_fieldname('vendors_slug')+'/new/'
        + get_fieldname.get_fieldname('products_slug')+'/new/?$',
        'whats_fresh.whats_fresh_api.views.entry.products.product_ajax',
        name='product_ajax'),

    url(r'^entry/'+get_fieldname.get_fieldname('products_slug')+'/?$',
        'whats_fresh.whats_fresh_api.views.entry.products.product_list',
        name='entry-list-products'),

    url(r'^entry/'+get_fieldname.get_fieldname('stories_slug')
        + '/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.entry.stories.story',
        name='edit-story'),

    url(r'^entry/'+get_fieldname.get_fieldname('stories_slug')+'/new/?$',
        'whats_fresh.whats_fresh_api.views.entry.stories.story',
        name='new-story'),

    url(r'^entry/'+get_fieldname.get_fieldname('stories_slug')+'/?$',
        'whats_fresh.whats_fresh_api.views.entry.stories.story_list',
        name='entry-list-stories'),

    # Endpoint for image popup in story.html
    url(r'^entry/'+get_fieldname.get_fieldname('stories_slug')+'/new/'
        + get_fieldname.get_fieldname('images_slug')+'/new/?$',
        'whats_fresh.whats_fresh_api.views.entry.images.image_ajax',
        name='image_ajax'),

    # Endpoint for video popup in story.html
    url(r'^entry/'+get_fieldname.get_fieldname('stories_slug')+'/new/'
        + get_fieldname.get_fieldname('videos_slug')+'/new/?$',
        'whats_fresh.whats_fresh_api.views.entry.videos.video_ajax',
        name='video_ajax'),

    url(r'^entry/'+get_fieldname.get_fieldname('preparations_slug')+'/new/?$',
        'whats_fresh.whats_fresh_api.views.entry.preparations.preparation',
        name='new-preparation'),

    url(r'^entry/'+get_fieldname.get_fieldname('preparations_slug')
        + '/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.entry.preparations.preparation',
        name='edit-preparation'),

    url(r'^entry/'+get_fieldname.get_fieldname('preparations_slug')+'/?$',
        'whats_fresh.whats_fresh_api.views.entry.preparations.prep_list',
        name='entry-list-preparations'),

    url(r'^entry/'+get_fieldname.get_fieldname('images_slug')
        + '/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.entry.images.image',
        name='edit-image'),

    url(r'^entry/'+get_fieldname.get_fieldname('images_slug')+'/?$',
        'whats_fresh.whats_fresh_api.views.entry.images.image_list',
        name='entry-list-images'),

    url(r'^entry/'+get_fieldname.get_fieldname('images_slug')+'/new/?$',
        'whats_fresh.whats_fresh_api.views.entry.images.image',
        name='new-image'),

    url(r'^entry/'+get_fieldname.get_fieldname('videos_slug')
        + '/(?P<id>\d+)/?$',
        'whats_fresh.whats_fresh_api.views.entry.videos.video',
        name='edit-video'),

    url(r'^entry/'+get_fieldname.get_fieldname('videos_slug')+'/?$',
        'whats_fresh.whats_fresh_api.views.entry.videos.video_list',
        name='entry-list-videos'),

    url(r'^entry/'+get_fieldname.get_fieldname('videos_slug')+'/new/?$',
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

admin.site.site_header = get_fieldname.get_fieldname('site_title') + ' administration'
