from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from whats_fresh_api.models import *
from django.contrib.gis.db import models
import json


class LocationTestCase(TestCase):
    """
    Test whether the /vendors/ and /vendors/products/<id> views
    return the correct results when given a coordinate to center on.

    For future test-writers: the location_fixtures tests have six vendors
    in them -- two in Newport, two in Waldport, and two in Portland. Each
    vendor has one product, and each product is sold at one of the two vendors
    in the city.

    This means you can easily test the proximity limit by limiting yourself
    to one city, or just the coast, etc.
    """
    fixtures = ['location_fixtures']

    # These tests are made assuming a proximity of 20. If this default value
    # is changed, then the tests would break without overriding it.
    @override_settings(DEFAULT_PROXIMITY='20')

    def setUp(self):
        # All fish around Newport
        # This JSON contains the four stores in Newport and Waldport,
        # but not the Portland ones.
        self.expected_all_products = """
{
  "error": {
    "error_level": null,
    "error_status": false,
    "error_name": null,
    "error_text": null
  },
  "vendors": [{
    "id": 3,
    "website": "",
    "street": "146 SE Bay Blvd",
    "contact_name": "Newport Tuna Contact",
    "city": "Newport",
    "story": 2,
    "zip": "97365",
    "location_description": "Located on Bay Blvd in Newport",
    "long": -124.050122,
    "state": "OR",
    "email": "",
    "status": true,
    "updated": "2014-08-08 23:27:05.568395+00:00",
    "description": "Fake Newport Tuna",
    "phone": null,
    "lat": 44.631592,
    "name": "Newport Tuna",
    "created": "2014-08-08 23:27:05.568395+00:00",
    "ext": {
      
    },
    "products": [
      {
        "id": 2,
        "preparation": "Frozen",
        "name": "Tuna"
      }
    ]
  },
  {
    "id": 5,
    "website": "",
    "street": "522 NW Spring St",
    "contact_name": "Waldport Tuna Contact",
    "city": "Waldport",
    "story": 2,
    "zip": "97394",
    "location_description": "Located on Spring St in Waldport",
    "long": -124.066166,
    "state": "OR",
    "email": "",
    "status": true,
    "updated": "2014-08-08 23:27:05.568395+00:00",
    "description": "Fake Waldport Tuna",
    "phone": null,
    "lat": 44.427761,
    "name": "Waldport Tuna",
    "created": "2014-08-08 23:27:05.568395+00:00",
    "ext": {
      
    },
    "products": [
      {
        "id": 2,
        "preparation": "Frozen",
        "name": "Tuna"
      }
    ]
  },
  {
    "id": 4,
    "website": "",
    "street": "1226 Oregon Coast Hwy",
    "contact_name": "Newpotr Halibut Contact",
    "city": "Newport",
    "story": 1,
    "zip": "97365",
    "location_description": "Located on Oregon Coast Hwy in Newport",
    "long": -124.052868,
    "state": "OR",
    "email": "",
    "status": true,
    "updated": "2014-08-08 23:27:05.568395+00:00",
    "description": "Fake Newport Halibut",
    "phone": null,
    "lat": 44.646006,
    "name": "Newport Halibut",
    "created": "2014-08-08 23:27:05.568395+00:00",
    "ext": {
      
    },
    "products": [
      {
        "id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  },
  {
    "id": 6,
    "website": "",
    "street": "190 SW Maple St",
    "contact_name": "Waldport Halibut Contact",
    "city": "Waldport",
    "story": 1,
    "zip": "97364",
    "location_description": "Located on SW Maple St in Waldport",
    "long": -124.069126,
    "state": "OR",
    "email": "",
    "status": true,
    "updated": "2014-08-08 23:27:05.568395+00:00",
    "description": "Fake Waldport Halibut",
    "phone": null,
    "lat": 44.425188,
    "name": "Waldport Halibut",
    "created": "2014-08-08 23:27:05.568395+00:00",
    "ext": {
      
    },
    "products": [
      {
        "id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  }]
}"""

        # Nearby vendors for product Halibut (1)
        # This JSON contains the two halibut stores in Newport and Waldport,
        # but not Portland. This is the return for a good coordinates.
        self.expected_halibut = """
{
  "error": {
    "error_level": null,
    "error_status": false,
    "error_name": null,
    "error_text": null
  },
  "vendors": [{
    "id": 4,
    "website": "",
    "street": "1226 Oregon Coast Hwy",
    "contact_name": "Newpotr Halibut Contact",
    "city": "Newport",
    "story": 1,
    "zip": "97365",
    "location_description": "Located on Oregon Coast Hwy in Newport",
    "long": -124.052868,
    "state": "OR",
    "email": "",
    "status": true,
    "updated": "2014-08-08 23:27:05.568395+00:00",
    "description": "Fake Newport Halibut",
    "phone": null,
    "lat": 44.646006,
    "name": "Newport Halibut",
    "created": "2014-08-08 23:27:05.568395+00:00",
    "ext": {
      
    },
    "products": {
      "1": {
        "preparation": "Frozen",
        "name": "Halibut"
      }
    }
  },
  {
    "id": 6,
    "website": "",
    "street": "190 SW Maple St",
    "contact_name": "Waldport Halibut Contact",
    "city": "Waldport",
    "story": 1,
    "zip": "97364",
    "location_description": "Located on SW Maple St in Waldport",
    "long": -124.069126,
    "state": "OR",
    "email": "",
    "status": true,
    "updated": "2014-08-08 23:27:05.568395+00:00",
    "description": "Fake Waldport Halibut",
    "phone": null,
    "lat": 44.425188,
    "name": "Waldport Halibut",
    "created": "2014-08-08 23:27:05.568395+00:00",
    "ext": {
      
    },
    "products": [
      {
        "id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  }]
}"""

        # All vendors for product Halibut (1)
        # This JSON contains the three halibut stores in Newport, Waldport,
        # and Portland. This is the return for a bad coordinates.
        self.expected_all_vendors_products = """
{
  "error": {
    "error_level": "Warning",
    "error_status": true,
    "error_name": "Bad location",
    "error_text": "String or unicode input unrecognized as WKT EWKT, and HEXEWKB."
  },
  "vendors": [{
    "id": 2,
    "name": "Portland Halibut",
    "status": true,
    "description": "Fake Portland Halibut",
    "lat": 45.520988,
    "long": -122.670619, 
    "street": "1 SW Pine St",
    "city": "Portland",
    "state": "OR",
    "zip": "97204",
    "location_description": "Located on Pine in Portland",
    "contact_name": "Portland Halibut Contact",
    "phone": null,
    "story": 1,
    "website": "",
    "email": "",
    "created": "2014-08-08 23:27:05.568395+00:00",
    "updated": "2014-08-08 23:27:05.568395+00:00",
    "ext": {
      
    },
    "products": {
      "1": {
        "preparation": "Frozen",
        "name": "Halibut"
      }
    }
  },{
    "id": 4,
    "website": "",
    "street": "1226 Oregon Coast Hwy",
    "contact_name": "Newpotr Halibut Contact",
    "city": "Newport",
    "story": 1,
    "zip": "97365",
    "location_description": "Located on Oregon Coast Hwy in Newport",
    "long": -124.052868,
    "state": "OR",
    "email": "",
    "status": true,
    "updated": "2014-08-08 23:27:05.568395+00:00",
    "description": "Fake Newport Halibut",
    "phone": null,
    "lat": 44.646006,
    "name": "Newport Halibut",
    "created": "2014-08-08 23:27:05.568395+00:00",
    "ext": {
      
    },
    "products": {
      "1": {
        "preparation": "Frozen",
        "name": "Halibut"
      }
    }
  },
  {
    "id": 6,
    "website": "",
    "street": "190 SW Maple St",
    "contact_name": "Waldport Halibut Contact",
    "city": "Waldport",
    "story": 1,
    "zip": "97364",
    "location_description": "Located on SW Maple St in Waldport",
    "long": -124.069126,
    "state": "OR",
    "email": "",
    "status": true,
    "updated": "2014-08-08 23:27:05.568395+00:00",
    "description": "Fake Waldport Halibut",
    "phone": null,
    "lat": 44.425188,
    "name": "Waldport Halibut",
    "created": "2014-08-08 23:27:05.568395+00:00",
    "ext": {
      
    },
    "products": [
      {
        "id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  }]
}"""

        # No vendors. This is the return for location queries from
        # the middle of nowhere.
        self.expected_no_vendors = """
{
  "error": {
    "error_level": null,
    "error_status": false,
    "error_name": null,
    "error_text": null
  },
  "vendors": []
}"""

        # All vendors for all products
        # This JSON contains the six fish stores in Newport, Waldport,
        # and Portland. This is the return for a bad coordinates.
        self.expected_error_result = """
{
  "error": {
    "error_level": "Warning",
    "error_status": true,
    "error_name": "Bad location",
    "error_text": "String or unicode input unrecognized as WKT EWKT, and HEXEWKB."
  },
  "1": {
    "website": "",
    "street": "720 SW Broadway",
    "contact_name": "Portland Tuna Contact",
    "city": "Portland",
    "story": 2,
    "zip": "97204",
    "location_description": "Located on Broadway in Portland",
    "long": -122.67963,
    "state": "OR",
    "email": "",
    "status": true,
    "updated": "2014-08-08 23:27:05.568395+00:00",
    "description": "Fake Portland Tuna",
    "phone": null,
    "lat": 45.518962,
    "name": "Portland Tuna",
    "created": "2014-08-08 23:27:05.568395+00:00",
    "ext": {
      
    },
    "products": {
      "2": {
        "preparation": "Frozen",
        "name": "Tuna"
      }
    }
  },
  "3": {
    "website": "",
    "street": "146 SE Bay Blvd",
    "contact_name": "Newport Tuna Contact",
    "city": "Newport",
    "story": 2,
    "zip": "97365",
    "location_description": "Located on Bay Blvd in Newport",
    "long": -124.050122,
    "state": "OR",
    "email": "",
    "status": true,
    "updated": "2014-08-08 23:27:05.568395+00:00",
    "description": "Fake Newport Tuna",
    "phone": null,
    "lat": 44.631592,
    "name": "Newport Tuna",
    "created": "2014-08-08 23:27:05.568395+00:00",
    "ext": {
      
    },
    "products": {
      "2": {
        "preparation": "Frozen",
        "name": "Tuna"
      }
    }
  },
  "2": {
    "website": "",
    "street": "1 SW Pine St",
    "contact_name": "Portland Halibut Contact",
    "city": "Portland",
    "story": 1,
    "zip": "97204",
    "location_description": "Located on Pine in Portland",
    "long": -122.670619,
    "state": "OR",
    "email": "",
    "status": true,
    "updated": "2014-08-08 23:27:05.568395+00:00",
    "description": "Fake Portland Halibut",
    "phone": null,
    "lat": 45.520988,
    "name": "Portland Halibut",
    "created": "2014-08-08 23:27:05.568395+00:00",
    "ext": {
      
    },
    "products": {
      "1": {
        "preparation": "Frozen",
        "name": "Halibut"
      }
    }
  },
  "5": {
    "website": "",
    "street": "522 NW Spring St",
    "contact_name": "Waldport Tuna Contact",
    "city": "Waldport",
    "story": 2,
    "zip": "97394",
    "location_description": "Located on Spring St in Waldport",
    "long": -124.066166,
    "state": "OR",
    "email": "",
    "status": true,
    "updated": "2014-08-08 23:27:05.568395+00:00",
    "description": "Fake Waldport Tuna",
    "phone": null,
    "lat": 44.427761,
    "name": "Waldport Tuna",
    "created": "2014-08-08 23:27:05.568395+00:00",
    "ext": {
      
    },
    "products": {
      "2": {
        "preparation": "Frozen",
        "name": "Tuna"
      }
    }
  },
  "4": {
    "website": "",
    "street": "1226 Oregon Coast Hwy",
    "contact_name": "Newpotr Halibut Contact",
    "city": "Newport",
    "story": 1,
    "zip": "97365",
    "location_description": "Located on Oregon Coast Hwy in Newport",
    "long": -124.052868,
    "state": "OR",
    "email": "",
    "status": true,
    "updated": "2014-08-08 23:27:05.568395+00:00",
    "description": "Fake Newport Halibut",
    "phone": null,
    "lat": 44.646006,
    "name": "Newport Halibut",
    "created": "2014-08-08 23:27:05.568395+00:00",
    "ext": {
      
    },
    "products": {
      "1": {
        "preparation": "Frozen",
        "name": "Halibut"
      }
    }
  },
  "6": {
    "website": "",
    "street": "190 SW Maple St",
    "contact_name": "Waldport Halibut Contact",
    "city": "Waldport",
    "story": 1,
    "zip": "97364",
    "location_description": "Located on SW Maple St in Waldport",
    "long": -124.069126,
    "state": "OR",
    "email": "",
    "status": true,
    "updated": "2014-08-08 23:27:05.568395+00:00",
    "description": "Fake Waldport Halibut",
    "phone": null,
    "lat": 44.425188,
    "name": "Waldport Halibut",
    "created": "2014-08-08 23:27:05.568395+00:00",
    "ext": {
      
    },
    "products": {
      "1": {
        "preparation": "Frozen",
        "name": "Halibut"
      }
    }
  }
}"""

    def test_successful_location_by_vendor_product(self):
        """
        Test that good parameters return vendor/product results ordered by
        location. There will also be a default limit of 20 miles.
        """
        halibut_near_newport = (self.client.get(
            '%s?lat=44.609079&long=-124.052538' % reverse('vendors-products',
                                                     kwargs={'id': '1'})
            ).content)

        expected_answer = json.loads(self.expected_halibut)
        self.assertEqual(halibut_near_newport, expected_answer)

    def test_successful_location_all_products(self):
        """
        Test that good parameters return all vendors ordered by location.
        There will also be a default limit of 20 miles.
        """
        all_vendors_data = json.loads(self.client.get(
            '%s?lat=44.609079&long=-124.052538' % reverse('vendors-list')
            ).content)

        expected_answer = json.loads(self.expected_all_products)
        self.assertEqual(all_vendors_data, expected_answer)

    def test_bad_location_parameters(self):
        """
        Test that only one parameter (only lat/only long) returns a Warning,
        and that bad parameter values (text) return Warning.
        """

        # Coordinates are not numbers
        all_vendors_data = json.loads(self.client.get(
            '%s?lat=not_a_latitude&long=not_a_longitude' % reverse('vendors-list')
            ).content)

        expected_answer = json.loads(self.expected_all_products)
        self.assertEqual(all_vendors_data, expected_answer)

    def test_no_vendors_nearby(self):
        """
        Test that, when there are no vendors, we get an empty list back.
        """
        all_vendors_data = json.loads(self.client.get(
            '%s?lat=44.015225&long=-123.016873' % reverse('vendors-list')
            ).content)

        expected_answer = json.loads(self.expected_no_vendors)
        self.assertEqual(all_vendors_data, expected_answer)

    def test_bad_location_parameters_vendor_products(self):
        """
        Test that only one parameter (only lat/only long) returns a Warning,
        and that bad parameter values (text) return Warning, for the
        vendors/products endpoint.
        """

        # Coordinates are not numbers
        broken_data = json.loads(self.client.get(
            '%s?lat=not_a_latitude&long=not_a_longitude' % reverse('vendors-list')
            ).content)

        expected_answer = json.loads(self.expected_all_vendors_products)
        self.assertEqual(broken_data, expected_answer)

    def test_no_vendors_nearby_vendor_products(self):
        """
        Test that, when there are no vendors, we get an empty list back for the
        vendors/products endpoint.
        """
        no_vendor_data = json.loads(
        self.client.get(
            '%s?lat=44.015225&long=-123.016873' % reverse(
                'vendors-products', kwargs={'id': '1'})
        ).content)

        expected_answer = json.loads(self.expected_no_vendors)
        self.assertEqual(all_vendors_data, expected_answer)
