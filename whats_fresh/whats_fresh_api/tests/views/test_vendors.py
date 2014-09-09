from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from whats_fresh_api.models import *
from django.contrib.gis.db import models
import json


class VendorsTestCase(TestCase):
    fixtures = ['test_fixtures']

    def setUp(self):
        self.expected_list = """
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
      "id": 1,
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
      "story_id":  1,
      "ext": {

      },
      "created": "2014-08-08 23:27:05.568395+00:00",
      "updated": "2014-08-08 23:27:05.568395+00:00",
      "products": [
        {
          "product_id": 2,
          "name": "Starfish Voyager",
          "preparation": "Live",
          "preparation_id": 1
        },
        {
          "product_id": 1,
          "name": "Ezri Dax",
          "preparation": "Live",
          "preparation_id": 1
        }
      ]
    },
{
 "id": 2,
        "name": "All Optional Null Fields Are Null",
        "status": null,
        "description": "Ceci n'est pas un magasin.",
        "lat": 37.833688,
        "long": -122.478002,
        "street": "501 Isabelle Rd",
        "city": "North Bend",
        "state": "OR",
        "zip": "97459",
        "location_description": "",
        "contact_name": "Isabelle",
        "phone": null,
        "hours": "",
        "website": "",
        "email": "",
        "story_id":  null,
        "ext": {},
        "created": "2014-08-08 23:27:05.568395+00:00",
        "updated": "2014-08-08 23:27:05.568395+00:00",
        "products": [
            {
                "product_id": 1,
                "name": "Ezri Dax",
                "preparation": "Live",
                "preparation_id": 1
            }
        ]
    }

  ]
}
"""

    def test_url_endpoint(self):
        url = reverse('vendors-list')
        self.assertEqual(url, '/vendors')

    def test_no_parameters(self):
        c = Client()
        response = self.client.get(reverse('vendors-list')).content
        parsed_answer = json.loads(response)

        expected_answer = json.loads(self.expected_list)

        self.maxDiff = None
        self.assertEqual(parsed_answer, expected_answer)


class NoVendorViewTestCase(TestCase):
    def setUp(self):
        self.expected_no_vendors = """
{
  "error": {
    "status": true,
    "text": "No Vendors found",
    "name": "No Vendors",
    "debug": "",
    "level": "Error"
  },
  "vendors": []
}"""

    def test_no_products(self):
        response = self.client.get(reverse('vendors-list'))

        parsed_answer = json.loads(response.content)
        expected_answer = json.loads(self.expected_no_vendors)
        self.assertEqual(response.status_code, 404)

        expected_answer = json.loads(self.expected_no_vendors)

        self.maxDiff = None

        self.assertEqual(parsed_answer, expected_answer)


class VendorsLocationTestCase(TestCase):
    """
    Test whether the /vendors/ view returns the correct results when given a
    coordinate to center on.

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
            "text": "No Vendors found",
            "name": "No Vendors"
  },
  "vendors": []
}"""

        # All fish around Newport
        # This JSON contains the four stores in Newport and Waldport,
        # but not the Portland ones.
        self.expected_nearby_all = """
{
  "error": {
    "level": null,
    "status": false,
    "name": null,
    "debug": null,
    "text": null
  },
  "vendors": [{
    "id": 3,
    "website": "",
    "street": "146 SE Bay Blvd",
    "contact_name": "Newport Tuna Contact",
    "city": "Newport",
    "story_id":  2,
    "zip": "97365",
    "location_description": "Located on Bay Blvd in Newport",
    "long": -124.050122,
    "state": "OR",
    "email": "",
    "hours": "",
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
        "product_id": 2,
        "preparation_id": 1,
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
    "id": 5,
    "website": "",
    "street": "522 NW Spring St",
    "contact_name": "Waldport Tuna Contact",
    "city": "Waldport",
    "story_id":  2,
    "zip": "97394",
    "location_description": "Located on Spring St in Waldport",
    "long": -124.066166,
    "state": "OR",
    "email": "",
    "hours": "",
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
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
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

        # All fish around Newport, with extended proximity.
        # This JSON contains the six stores in Newport, Waldport, Pacific City
        # but not the Portland ones.
        self.expected_nearby_extended = """
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
      "description": "Fake Newport Tuna",
      "zip": "97365",
      "created": "2014-08-08 23:27:05.568395+00:00",
      "story_id": 2,
      "ext": {

      },
      "location_description": "Located on Bay Blvd in Newport",
      "long": -124.050122,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "146 SE Bay Blvd",
      "products": [
        {
          "preparation": "Frozen",
          "preparation_id": 1,
          "product_id": 2,
          "name": "Tuna"
        }
      ],
      "lat": 44.631592,
      "contact_name": "Newport Tuna Contact",
      "id": 3,
      "name": "Newport Tuna"
    },
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
      "description": "Fake Waldport Tuna",
      "zip": "97394",
      "created": "2014-08-08 23:27:05.568395+00:00",
      "story_id": 2,
      "ext": {

      },
      "location_description": "Located on Spring St in Waldport",
      "long": -124.066166,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "522 NW Spring St",
      "products": [
        {
          "preparation": "Frozen",
          "preparation_id": 1,
          "product_id": 2,
          "name": "Tuna"
        }
      ],
      "lat": 44.427761,
      "contact_name": "Waldport Tuna Contact",
      "id": 5,
      "name": "Waldport Tuna"
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
      "description": "Fake Pacific City Tuna",
      "zip": "97112",
      "created": "2014-08-08 23:27:05.568395+00:00",
      "story_id": 2,
      "ext": {

      },
      "location_description": "Located on Roger Ave in Pacific City",
      "long": -123.958093,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "35650 Roger Ave",
      "products": [

      ],
      "lat": 45.197105,
      "contact_name": "Pacific City Tuna Contact",
      "id": 7,
      "name": "Pacific City Tuna"
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

      ],
      "lat": 45.207253,
      "contact_name": "Pacific City Halibut Contact",
      "id": 8,
      "name": "Pacific City Halibut"
    }
  ]
}"""

        # All vendors for all products
        # This JSON contains the six fish stores in Newport, Waldport,
        # and Portland. This is the return for a bad coordinates.
        self.expected_error_result = """
{
  "error": {
    "level": "Warning",
    "status": true,
    "text": "There was an error with the given coordinates not_a_latitude, not_a_longitude",
    "name": "Bad location",
    "debug": "String or unicode input unrecognized as WKT EWKT, and HEXEWKB."
  },
  "vendors": [
  {
    "id": 1,
    "website": "",
    "street": "720 SW Broadway",
    "contact_name": "Portland Tuna Contact",
    "city": "Portland",
    "story_id":  2,
    "zip": "97204",
    "location_description": "Located on Broadway in Portland",
    "long": -122.67963,
    "state": "OR",
    "email": "",
    "hours": "",
    "status": true,
    "updated": "2014-08-08 23:27:05.568395+00:00",
    "description": "Fake Portland Tuna",
    "phone": null,
    "lat": 45.518962,
    "name": "Portland Tuna",
    "created": "2014-08-08 23:27:05.568395+00:00",
    "ext": {

    },
    "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
    ]
  },
  {
    "id": 3,
    "website": "",
    "street": "146 SE Bay Blvd",
    "contact_name": "Newport Tuna Contact",
    "city": "Newport",
    "story_id":  2,
    "zip": "97365",
    "location_description": "Located on Bay Blvd in Newport",
    "long": -124.050122,
    "state": "OR",
    "email": "",
    "hours": "",
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
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
    ]
  },
  {
    "id": 2,
    "website": "",
    "street": "1 SW Pine St",
    "contact_name": "Portland Halibut Contact",
    "city": "Portland",
    "story_id":  1,
    "zip": "97204",
    "location_description": "Located on Pine in Portland",
    "long": -122.670619,
    "state": "OR",
    "hours": "",
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
    "products": [
      {
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  },
  {
    "id": 5,
    "website": "",
    "street": "522 NW Spring St",
    "contact_name": "Waldport Tuna Contact",
    "city": "Waldport",
    "story_id":  2,
    "zip": "97394",
    "location_description": "Located on Spring St in Waldport",
    "long": -124.066166,
    "state": "OR",
    "hours": "",
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
        "product_id": 2,
        "preparation_id": 1,
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
    "story_id":  1,
    "zip": "97365",
    "location_description": "Located on Oregon Coast Hwy in Newport",
    "long": -124.052868,
    "state": "OR",
    "hours": "",
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
        "product_id": 1,
        "preparation_id": 1,
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
    "hours": "",
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
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  },
    {
      "status": true,
      "city": "Cloverdale",
      "website": "",
      "updated": "2014-08-08 23:27:05.568395+00:00",
      "description": "Fake Pacific City Tuna",
      "zip": "97112",
      "created": "2014-08-08 23:27:05.568395+00:00",
      "story_id": 2,
      "ext": {

      },
      "location_description": "Located on Roger Ave in Pacific City",
      "long": -123.958093,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "35650 Roger Ave",
      "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
      ],
      "lat": 45.197105,
      "contact_name": "Pacific City Tuna Contact",
      "id": 7,
      "name": "Pacific City Tuna"
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
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
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

        # All vendors for all products
        # This JSON contains the six fish stores in Newport, Waldport,
        # and Portland. This is the return for a bad coordinates.
        self.expected_error_missing_long = """
{
  "error": {
    "level": "Warning",
    "status": true,
    "name": "Bad location",
    "text": "There was an error with the given coordinates -45.232, None",
    "debug": "Error encountered checking Geometry returned from GEOS C function \\"GEOSWKTReader_read_r\\"."
  },
  "vendors": [
  {
    "id": 1,
    "website": "",
    "street": "720 SW Broadway",
    "contact_name": "Portland Tuna Contact",
    "city": "Portland",
    "story_id":  2,
    "zip": "97204",
    "location_description": "Located on Broadway in Portland",
    "long": -122.67963,
    "state": "OR",
    "hours": "",
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
    "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
    ]
  },
  {
    "id": 3,
    "website": "",
    "street": "146 SE Bay Blvd",
    "contact_name": "Newport Tuna Contact",
    "city": "Newport",
    "story_id":  2,
    "zip": "97365",
    "location_description": "Located on Bay Blvd in Newport",
    "long": -124.050122,
    "state": "OR",
    "hours": "",
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
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
    ]
  },
  {
    "id": 2,
    "website": "",
    "street": "1 SW Pine St",
    "contact_name": "Portland Halibut Contact",
    "city": "Portland",
    "story_id":  1,
    "zip": "97204",
    "location_description": "Located on Pine in Portland",
    "long": -122.670619,
    "state": "OR",
    "hours": "",
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
    "products": [
      {
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  },
  {
    "id": 5,
    "website": "",
    "street": "522 NW Spring St",
    "contact_name": "Waldport Tuna Contact",
    "city": "Waldport",
    "story_id":  2,
    "zip": "97394",
    "location_description": "Located on Spring St in Waldport",
    "long": -124.066166,
    "state": "OR",
    "hours": "",
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
        "product_id": 2,
        "preparation_id": 1,
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
    "story_id":  1,
    "zip": "97365",
    "location_description": "Located on Oregon Coast Hwy in Newport",
    "long": -124.052868,
    "state": "OR",
    "hours": "",
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
        "product_id": 1,
        "preparation_id": 1,
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
    "hours": "",
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
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  },
    {
      "status": true,
      "city": "Cloverdale",
      "website": "",
      "updated": "2014-08-08 23:27:05.568395+00:00",
      "description": "Fake Pacific City Tuna",
      "zip": "97112",
      "created": "2014-08-08 23:27:05.568395+00:00",
      "story_id": 2,
      "ext": {

      },
      "location_description": "Located on Roger Ave in Pacific City",
      "long": -123.958093,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "35650 Roger Ave",
      "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
      ],
      "lat": 45.197105,
      "contact_name": "Pacific City Tuna Contact",
      "id": 7,
      "name": "Pacific City Tuna"
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
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
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

        # All vendors for all products
        # This JSON contains the six fish stores in Newport, Waldport,
        # and Portland. This is the return for a bad coordinates.
        self.expected_error_missing_lat = """
{
  "error": {
    "level": "Warning",
    "status": true,
    "name": "Bad location",
    "text": "There was an error with the given coordinates None, -45.232",
    "debug": "Error encountered checking Geometry returned from GEOS C function \\"GEOSWKTReader_read_r\\"."
  },
  "vendors": [
  {
    "id": 1,
    "website": "",
    "street": "720 SW Broadway",
    "contact_name": "Portland Tuna Contact",
    "city": "Portland",
    "story_id":  2,
    "zip": "97204",
    "location_description": "Located on Broadway in Portland",
    "long": -122.67963,
    "state": "OR",
    "hours": "",
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
    "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
    ]
  },
  {
    "id": 3,
    "website": "",
    "street": "146 SE Bay Blvd",
    "contact_name": "Newport Tuna Contact",
    "city": "Newport",
    "story_id":  2,
    "zip": "97365",
    "location_description": "Located on Bay Blvd in Newport",
    "long": -124.050122,
    "state": "OR",
    "hours": "",
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
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
    ]
  },
  {
    "id": 2,
    "website": "",
    "street": "1 SW Pine St",
    "contact_name": "Portland Halibut Contact",
    "city": "Portland",
    "story_id":  1,
    "zip": "97204",
    "location_description": "Located on Pine in Portland",
    "long": -122.670619,
    "state": "OR",
    "hours": "",
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
    "products": [
      {
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  },
  {
    "id": 5,
    "website": "",
    "street": "522 NW Spring St",
    "contact_name": "Waldport Tuna Contact",
    "city": "Waldport",
    "story_id":  2,
    "zip": "97394",
    "location_description": "Located on Spring St in Waldport",
    "long": -124.066166,
    "state": "OR",
    "hours": "",
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
        "product_id": 2,
        "preparation_id": 1,
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
    "story_id":  1,
    "zip": "97365",
    "location_description": "Located on Oregon Coast Hwy in Newport",
    "long": -124.052868,
    "state": "OR",
    "hours": "",
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
        "product_id": 1,
        "preparation_id": 1,
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
    "hours": "",
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
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  },
    {
      "status": true,
      "city": "Cloverdale",
      "website": "",
      "updated": "2014-08-08 23:27:05.568395+00:00",
      "description": "Fake Pacific City Tuna",
      "zip": "97112",
      "created": "2014-08-08 23:27:05.568395+00:00",
      "story_id": 2,
      "ext": {

      },
      "location_description": "Located on Roger Ave in Pacific City",
      "long": -123.958093,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "35650 Roger Ave",
      "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
      ],
      "lat": 45.197105,
      "contact_name": "Pacific City Tuna Contact",
      "id": 7,
      "name": "Pacific City Tuna"
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
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
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

    def test_successful_location_all_products(self):
        """
        Test that good parameters return all vendors ordered by location.
        There will also be a default limit of 20 miles.
        """
        all_vendors_data = json.loads(self.client.get(
            '%s?lat=44.609079&long=-124.052538' % reverse('vendors-list')
            ).content)

        expected_answer = json.loads(self.expected_nearby_all)
        self.assertEqual(all_vendors_data, expected_answer)

    def test_good_proximity_all_products(self):
        """
        Test that good parameters return all vendors ordered by location.
        Extending the proximity to 50 miles adds two stores.
        """
        extended_proximity = json.loads(self.client.get(
            '%s?lat=44.609079&long=-124.052538&' \
                'proximity=50' % reverse('vendors-list')
            ).content)

        expected_answer = json.loads(self.expected_nearby_extended)
        self.assertEqual(extended_proximity, expected_answer)

    def test_bad_location_with_proximity_parameters(self):
        """
        Test that a bad location returns an error with good proximity.
        """
        all_vendors_data = json.loads(self.client.get(
            '%s?lat=not_a_latitude&long=not_a_longitude&' \
                'proximity=50' % reverse('vendors-list')
            ).content)

        expected_answer = json.loads(self.expected_error_result)

        all_vendors_data['vendors'] = sorted(
            all_vendors_data['vendors'], key=lambda k: k['id'])
        expected_answer['vendors'] = sorted(
            expected_answer['vendors'], key=lambda k: k['id'])

        self.assertEqual(all_vendors_data, expected_answer)

    def test_bad_location_parameters(self):
        """
        Test that only one parameter (only lat/only long) returns a Warning,
        and that bad parameter values (text) return Warning.
        """

        # Coordinates are not numbers
        all_vendors_data = json.loads(self.client.get(
            '%s?lat=not_a_latitude&long=not_a_longitude' % reverse(
                'vendors-list')
            ).content)

        expected_answer = json.loads(self.expected_error_result)

        all_vendors_data['vendors'] = sorted(
            all_vendors_data['vendors'], key=lambda k: k['id'])
        expected_answer['vendors'] = sorted(
            expected_answer['vendors'], key=lambda k: k['id'])

        for vendor in all_vendors_data['vendors']:
            for product in vendor['products']:
                self.assertTrue('product_id' in product)

        for vendor in expected_answer['vendors']:
            vendor['products'] = sorted(
                vendor['products'], key=lambda k: k['product_id'])

        for vendor in all_vendors_data['vendors']:
            vendor['products'] = sorted(
                vendor['products'], key=lambda k: k['product_id'])

        self.assertEqual(all_vendors_data, expected_answer)

        # Lat is missing
        expected_answer = json.loads(self.expected_error_missing_lat)

        all_vendors_data = json.loads(self.client.get(
            '%s?long=-45.232' % reverse('vendors-list')
            ).content)

        all_vendors_data['vendors'] = sorted(
            all_vendors_data['vendors'], key=lambda k: k['id'])
        expected_answer['vendors'] = sorted(
            expected_answer['vendors'], key=lambda k: k['id'])

        for vendor in all_vendors_data['vendors']:
            for product in vendor['products']:
                self.assertTrue('product_id' in product)

        for vendor in expected_answer['vendors']:
            vendor['products'] = sorted(
                vendor['products'], key=lambda k: k['product_id'])

        for vendor in all_vendors_data['vendors']:
            vendor['products'] = sorted(
                vendor['products'], key=lambda k: k['product_id'])

        self.assertEqual(all_vendors_data, expected_answer)

        # Long is missing
        expected_answer = json.loads(self.expected_error_missing_long)

        all_vendors_data = json.loads(self.client.get(
            '%s?lat=-45.232' % reverse('vendors-list')
            ).content)
        all_vendors_data['vendors'] = sorted(
            all_vendors_data['vendors'], key=lambda k: k['id'])
        expected_answer['vendors'] = sorted(
            expected_answer['vendors'], key=lambda k: k['id'])

        for vendor in expected_answer['vendors']:
            vendor['products'] = sorted(
                vendor['products'], key=lambda k: k['product_id'])

        for vendor in all_vendors_data['vendors']:
            vendor['products'] = sorted(
                vendor['products'], key=lambda k: k['product_id'])

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
