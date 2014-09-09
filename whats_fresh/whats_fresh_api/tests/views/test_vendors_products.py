from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from whats_fresh_api.models import *
from django.contrib.gis.db import models
from django.test.utils import override_settings
import json


class VendorsProductsTestCase(TestCase):
    fixtures = ['overlapping_fixtures']

    def setUp(self):
        self.maxDiff = None
        self.expected_json = """
{
  "error": {
    "status": false,
    "name": null,
    "text": null,
    "debug": null,
    "level": null
  },
  "vendors": [
    {
      "id": 10,
      "name": "No Optional Null Fields Are Null",
      "status": true,
      "description": "This is a vendor shop.",
      "lat": 37.833688,
      "long": -122.478002,
      "street": "1633 Sommerville Rd",
      "city": "Sausalito",
      "state": "CA",
      "zip": "94965",
      "hours": "Open Tuesday, 10am to 5pm",
      "location_description": "Location description",
      "contact_name": "A. Persson",
      "phone": 5417377627,
      "website": "http://example.com",
      "email": "a@perr.com",
      "story_id":  10,
      "ext": {

      },
      "created": "2014-08-08 23:27:05.568395+00:00",
      "updated": "2014-08-08 23:27:05.568395+00:00",
      "products": [
        {
          "product_id": 10,
          "name": "Starfish Voyager",
          "preparation": "Live",
          "preparation_id": 10
        },
        {
          "product_id": 100,
          "name": "Ezri Dax",
          "preparation": "Live",
          "preparation_id": 10
        }
      ]
    }
  ]
}"""

    def test_url_endpoint(self):
        url = reverse('vendors-products', kwargs={'id': '10'})
        self.assertEqual(url, '/vendors/products/10')

    def test_no_location_parameter(self):
        c = Client()
        response = c.get(
            reverse('vendors-products', kwargs={'id': '10'})).content
        parsed_answer = json.loads(response)

        expected_answer = json.loads(self.expected_json)

        parsed_answer['vendors'] = sorted(
            parsed_answer['vendors'], key=lambda k: k['id'])
        expected_answer['vendors'] = sorted(
            expected_answer['vendors'], key=lambda k: k['id'])

        for vendor in parsed_answer['vendors']:
            for product in vendor['products']:
                self.assertTrue('product_id' in product)

        for vendor in expected_answer['vendors']:
            vendor['products'] = sorted(
                vendor['products'], key=lambda k: k['product_id'])

        for vendor in parsed_answer['vendors']:
            vendor['products'] = sorted(
                vendor['products'], key=lambda k: k['product_id'])

        self.maxDiff = None

        self.assertEqual(parsed_answer, expected_answer)


class VendorsProductsLocationTestCase(TestCase):
    """
    Test whether the /vendors/products/<id> view returns the correct results
    when given a coordinate to center on.

    This is an individual class to allow the use of different fixture sets.

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
        self.maxDiff = None

        # No vendors. This is the return for location queries from
        # the middle of nowhere.
        self.expected_no_vendors = """
{
  "error": {
    "debug": "",
    "status": true,
    "level": "Error",
    "text": "No Vendors found for product 1",
    "name": "No Vendors"
    },
  "vendors": []
}"""

        # Nearby vendors for product Halibut (1)
        # This JSON contains the two halibut stores in Newport and Waldport,
        # but not Portland. This is the return for a good coordinates.
        self.expected_halibut = """
{
  "error": {
    "level": null,
    "status": false,
    "name": null,
    "debug": null,
    "text": null
  },
  "vendors": [{
    "id": 4,
    "website": "",
    "street": "1226 Oregon Coast Hwy",
    "contact_name": "Newpotr Halibut Contact",
    "city": "Newport",
    "story_id":  1,
    "zip": "97365",
    "location_description": "Located on Oregon Coast Hwy in Newport",
    "long": -124.052868,
    "state": "OR",
    "email": "",
    "hours": "",
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
        "product_id": 1,
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
    "story_id":  1,
    "zip": "97364",
    "location_description": "Located on SW Maple St in Waldport",
    "long": -124.069126,
    "state": "OR",
    "email": "",
    "hours": "",
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
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  }]
}"""

        # Nearby vendors for product Halibut (1), with 50 mile range.
        # This JSON contains the halibut stores in Newport, Waldport, and
        # Pacific City, but not Portland. This is the return for a good
        # coordinates.
        self.expected_halibut_extended = """
{
  "error": {
    "debug": null,
    "status": false,
    "text": null,
    "name": null,
    "level": null
  },
  "vendors": [
    {
      "status": true,
      "city": "Newport",
      "website": "",
      "updated": "2014-08-08 23:27:05.568395+00:00",
      "description": "Fake Newport Halibut",
      "zip": "97365",
      "created": "2014-08-08 23:27:05.568395+00:00",
      "story_id": 1,
      "ext": {

      },
      "location_description": "Located on Oregon Coast Hwy in Newport",
      "long": -124.052868,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "1226 Oregon Coast Hwy",
      "products": [
        {
          "preparation": "Frozen",
          "preparation_id": 1,
          "product_id": 1,
          "name": "Halibut"
        }
      ],
      "lat": 44.646006,
      "contact_name": "Newpotr Halibut Contact",
      "id": 4,
      "name": "Newport Halibut"
    },
    {
      "status": true,
      "city": "Waldport",
      "website": "",
      "updated": "2014-08-08 23:27:05.568395+00:00",
      "description": "Fake Waldport Halibut",
      "zip": "97364",
      "created": "2014-08-08 23:27:05.568395+00:00",
      "story_id": 1,
      "ext": {

      },
      "location_description": "Located on SW Maple St in Waldport",
      "long": -124.069126,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "190 SW Maple St",
      "products": [
        {
          "preparation": "Frozen",
          "preparation_id": 1,
          "product_id": 1,
          "name": "Halibut"
        }
      ],
      "lat": 44.425188,
      "contact_name": "Waldport Halibut Contact",
      "id": 6,
      "name": "Waldport Halibut"
    },
    {
      "status": true,
      "city": "Cloverdale",
      "website": "",
      "updated": "2014-08-08 23:27:05.568395+00:00",
      "description": "Fake Pacific City Halibut",
      "zip": "97112",
      "created": "2014-08-08 23:27:05.568395+00:00",
      "story_id": 1,
      "ext": {

      },
      "location_description": "Located on Brooten Rd in Pacific City",
      "long": -123.959418,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "34455 Brooten Rd",
      "products": [
        {
          "preparation": "Frozen",
          "preparation_id": 1,
          "product_id": 1,
          "name": "Halibut"
        }
      ],
      "lat": 45.207253,
      "contact_name": "Pacific City Halibut Contact",
      "id": 8,
      "name": "Pacific City Halibut"
    }
  ]
}"""

        # All vendors for product Halibut (1)
        # This JSON contains the three halibut stores in Newport, Waldport,
        # and Portland. This is the return for a bad coordinates.
        self.expected_all_vendors_products = """
{
  "error": {
    "level": "Warning",
    "status": true,
    "text": "There was an error with the given coordinates not_a_latitude, not_a_longitude",
    "name": "Bad location",
    "debug": "String or unicode input unrecognized as WKT EWKT, and HEXEWKB."
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
    "story_id":  1,
    "hours": "",
    "website": "",
    "email": "",
    "created": "2014-08-08 23:27:05.568395+00:00",
    "updated": "2014-08-08 23:27:05.568395+00:00",
    "ext": {

    },
    "products": [
      {
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  },{
    "id": 4,
    "website": "",
    "street": "1226 Oregon Coast Hwy",
    "contact_name": "Newpotr Halibut Contact",
    "city": "Newport",
    "story_id":  1,
    "zip": "97365",
    "location_description": "Located on Oregon Coast Hwy in Newport",
    "long": -124.052868,
    "state": "OR",
    "email": "",
    "hours": "",
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
        "product_id": 1,
        "preparation": "Frozen",
        "preparation_id": 1,
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
    "story_id":  1,
    "zip": "97364",
    "location_description": "Located on SW Maple St in Waldport",
    "long": -124.069126,
    "state": "OR",
    "email": "",
    "hours": "",
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
        "product_id": 1,
        "preparation": "Frozen",
        "preparation_id": 1,
        "name": "Halibut"
      }
    ]
  },
    {
      "status": true,
      "city": "Cloverdale",
      "website": "",
      "updated": "2014-08-08 23:27:05.568395+00:00",
      "description": "Fake Pacific City Halibut",
      "zip": "97112",
      "created": "2014-08-08 23:27:05.568395+00:00",
      "story_id": 1,
      "ext": {

      },
      "location_description": "Located on Brooten Rd in Pacific City",
      "long": -123.959418,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "34455 Brooten Rd",
      "products": [
        {
          "preparation": "Frozen",
          "preparation_id": 1,
          "product_id": 1,
          "name": "Halibut"
        }
      ],
      "lat": 45.207253,
      "contact_name": "Pacific City Halibut Contact",
      "id": 8,
      "name": "Pacific City Halibut"
    }]
}"""

        # All vendors for product Halibut (1)
        # This JSON contains the three halibut stores in Newport, Waldport,
        # and Portland. This is the return for a bad proximity with good
        # location -- the default proximity of 20 miles.
        self.expected_vp_bad_prox = """
{
  "error": {
    "level": "Warning",
    "status": true,
    "text": "There was an error finding vendors within cat miles",
    "name": "Bad proximity",
    "debug": "ValueError: invalid literal for int() with base 10: 'cat'"
  },
  "vendors": [{
    "id": 4,
    "website": "",
    "street": "1226 Oregon Coast Hwy",
    "contact_name": "Newpotr Halibut Contact",
    "city": "Newport",
    "story_id":  1,
    "zip": "97365",
    "location_description": "Located on Oregon Coast Hwy in Newport",
    "long": -124.052868,
    "state": "OR",
    "email": "",
    "hours": "",
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
        "product_id": 1,
        "preparation": "Frozen",
        "preparation_id": 1,
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
    "story_id":  1,
    "zip": "97364",
    "location_description": "Located on SW Maple St in Waldport",
    "long": -124.069126,
    "state": "OR",
    "email": "",
    "hours": "",
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
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  }]
}"""

        # All vendors for product Halibut (1)
        # This JSON contains the three halibut stores in Newport, Waldport,
        # and Portland. This is the return for a bad coordinates.
        self.expected_all_missing_long = """
{
  "error": {
    "level": "Warning",
    "status": true,
    "name": "Bad location",
    "text": "There was an error with the given coordinates -45.232, None",
    "debug": "Error encountered checking Geometry returned from GEOS C function \\"GEOSWKTReader_read_r\\"."
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
    "story_id":  1,
    "hours": "",
    "website": "",
    "email": "",
    "created": "2014-08-08 23:27:05.568395+00:00",
    "updated": "2014-08-08 23:27:05.568395+00:00",
    "ext": {

    },
    "products": [
      {
        "product_id": 1,
        "preparation": "Frozen",
        "preparation_id": 1,
        "name": "Halibut"
      }
    ]
  },{
    "id": 4,
    "website": "",
    "street": "1226 Oregon Coast Hwy",
    "contact_name": "Newpotr Halibut Contact",
    "city": "Newport",
    "story_id":  1,
    "zip": "97365",
    "location_description": "Located on Oregon Coast Hwy in Newport",
    "long": -124.052868,
    "state": "OR",
    "email": "",
    "hours": "",
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
        "product_id": 1,
        "preparation": "Frozen",
        "preparation_id": 1,
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
    "story_id":  1,
    "zip": "97364",
    "location_description": "Located on SW Maple St in Waldport",
    "long": -124.069126,
    "state": "OR",
    "email": "",
    "hours": "",
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
        "product_id": 1,
        "preparation": "Frozen",
        "preparation_id": 1,
        "name": "Halibut"
      }
    ]
  },
    {
      "status": true,
      "city": "Cloverdale",
      "website": "",
      "updated": "2014-08-08 23:27:05.568395+00:00",
      "description": "Fake Pacific City Halibut",
      "zip": "97112",
      "created": "2014-08-08 23:27:05.568395+00:00",
      "story_id": 1,
      "ext": {

      },
      "location_description": "Located on Brooten Rd in Pacific City",
      "long": -123.959418,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "34455 Brooten Rd",
      "products": [
        {
          "preparation": "Frozen",
          "preparation_id": 1,
          "product_id": 1,
          "name": "Halibut"
        }
      ],
      "lat": 45.207253,
      "contact_name": "Pacific City Halibut Contact",
      "id": 8,
      "name": "Pacific City Halibut"
    }]
}"""

        # All vendors for product Halibut (1)
        # This JSON contains the three halibut stores in Newport, Waldport,
        # and Portland. This is the return for a bad coordinates.
        self.expected_all_missing_lat = """
{
  "error": {
    "level": "Warning",
    "status": true,
    "name": "Bad location",
    "text": "There was an error with the given coordinates None, -45.232",
    "debug": "Error encountered checking Geometry returned from GEOS C function \\"GEOSWKTReader_read_r\\"."
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
    "story_id":  1,
    "hours": "",
    "website": "",
    "email": "",
    "created": "2014-08-08 23:27:05.568395+00:00",
    "updated": "2014-08-08 23:27:05.568395+00:00",
    "ext": {

    },
    "products": [
      {
        "product_id": 1,
        "preparation": "Frozen",
        "preparation_id": 1,
        "name": "Halibut"
      }
    ]
  },{
    "id": 4,
    "website": "",
    "street": "1226 Oregon Coast Hwy",
    "contact_name": "Newpotr Halibut Contact",
    "city": "Newport",
    "story_id":  1,
    "zip": "97365",
    "location_description": "Located on Oregon Coast Hwy in Newport",
    "long": -124.052868,
    "state": "OR",
    "email": "",
    "hours": "",
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
        "product_id": 1,
        "preparation": "Frozen",
        "preparation_id": 1,
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
    "story_id":  1,
    "zip": "97364",
    "location_description": "Located on SW Maple St in Waldport",
    "long": -124.069126,
    "state": "OR",
    "email": "",
    "hours": "",
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
        "product_id": 1,
        "preparation": "Frozen",
        "preparation_id": 1,
        "name": "Halibut"
      }
    ]
  },
    {
      "status": true,
      "city": "Cloverdale",
      "website": "",
      "updated": "2014-08-08 23:27:05.568395+00:00",
      "description": "Fake Pacific City Halibut",
      "zip": "97112",
      "created": "2014-08-08 23:27:05.568395+00:00",
      "story_id": 1,
      "ext": {

      },
      "location_description": "Located on Brooten Rd in Pacific City",
      "long": -123.959418,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "34455 Brooten Rd",
      "products": [
        {
          "preparation": "Frozen",
          "preparation_id": 1,
          "product_id": 1,
          "name": "Halibut"
        }
      ],
      "lat": 45.207253,
      "contact_name": "Pacific City Halibut Contact",
      "id": 8,
      "name": "Pacific City Halibut"
    }]
}"""

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
        self.assertEqual(no_vendor_data, expected_answer)

    def test_successful_location_by_vendor_product(self):
        """
        Test that good parameters return vendor/product results ordered by
        location. There will also be a default limit of 20 miles.
        """
        halibut_near_newport = self.client.get(
            '%s?lat=44.609079&long=-124.052538' % reverse('vendors-products',
                                                     kwargs={'id': '1'})
            ).content

        expected_answer = json.loads(self.expected_halibut)
        self.assertEqual(expected_answer, expected_answer)

    def test_bad_location_parameters_vendor_products(self):
        """
        Test that only one parameter (only lat/only long) returns a Warning,
        and that bad parameter values (text) return Warning, for the
        vendors/products endpoint.
        """

        # Coordinates are not numbers
        broken_data = json.loads(self.client.get(
            '%s?lat=not_a_latitude&long=not_a_longitude' % reverse(
                'vendors-products', kwargs={'id': '1'})
            ).content)

        expected_answer = json.loads(self.expected_all_vendors_products)
        self.assertEqual(broken_data, expected_answer)

        # lat is missing
        broken_data = json.loads(self.client.get(
            '%s?long=-45.232' % reverse(
                'vendors-products', kwargs={'id': '1'})
            ).content)
        expected_answer = json.loads(self.expected_all_missing_lat)

        self.assertEqual(broken_data, expected_answer)

        # long is missing
        broken_data = json.loads(self.client.get(
            '%s?lat=-45.232' % reverse(
                'vendors-products', kwargs={'id': '1'})
            ).content)
        expected_answer = json.loads(self.expected_all_missing_long)

        self.assertEqual(broken_data, expected_answer)

    def test_successful_location_by_vendor_product_extended_proximity(self):
        """
        Test that good parameters return vendor/product results ordered by
        location, with an extended proximity of 50 miles. This will include
        the Pacific City location.
        """
        halibut_near_newport_extended = json.loads(self.client.get(
            '%s?lat=44.609079&long=-124.052538' \
                '&proximity=50' % reverse(
                    'vendors-products', kwargs={'id': '1'})
            ).content)

        expected_answer = json.loads(self.expected_halibut_extended)
        self.assertEqual(halibut_near_newport_extended, expected_answer)

    def test_proximity_bad_location_vendor_products(self):
        """
        Test that bad location returns a Warning.
        """
        # Good proximity, bad location
        broken_data = json.loads(self.client.get(
            '%s?lat=not_a_latitude&long=not_a_longitude&proximity=50' % reverse(
                'vendors-products', kwargs={'id': '1'})
            ).content)

        expected_answer = json.loads(self.expected_all_vendors_products)
        self.assertEqual(broken_data, expected_answer)

    def test_bad_proximity_good_location_vendor_products(self):
        """
        Test that bad proximity returns a Warning.
        """
        broken_data = json.loads(self.client.get(
            '%s?lat=44.609079&long=-124.052538&proximity=cat' % reverse(
                'vendors-products', kwargs={'id': '1'})
            ).content)

        expected_answer = json.loads(self.expected_vp_bad_prox)
        self.assertEqual(broken_data, expected_answer)