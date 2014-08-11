from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^vendors/?$', 'whats_fresh_api.views.vendor.vendor_list', name='vendors-list'),
)
