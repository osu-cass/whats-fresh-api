from django.http import (HttpResponse,
                         HttpResponseNotFound,
                         HttpResponseServerError)
from whats_fresh_api.models import Vendor, Product, VendorProduct
from django.forms.models import model_to_dict

import json


def ProductVendor(request, id=None):
    
