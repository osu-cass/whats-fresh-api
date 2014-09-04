.. _api:

API Endpoints
=============

The What's Fresh API is a REST-style JSON API for Oregon Coast fish vendors.

The data can be accessed through a handful of endpoints:

.. contents:: `Endpoints`
   :depth: 1
   :local:

Every API return will include an ``error`` hash, containing an error status,
error name, error text, and error level. If the error status is True, the data
should be considered bad and ignored. The error name will return a
human-readable error name, like "Product Not Found", and the error text will
contain slightly more detail, including the ID of the object not found.

The API will only return HTTP 200 status codes, including for errors, except
in the case of server-side errors, which will return a 500.

  .. note:: In the future, it will be possible to get a short description of each endpoint by adding /describe to the end.
  .. note:: As of yet, none of the parameters have been added.

If future additions are made to the API, they will be made in the ``ext``
extension dictionary so as to provide backward compatibility.

Products listing
----------------

The products listing is available at ``/products/``. It returns a JSON array
consisting of each of the products, and information about them.

Optional Fields
^^^^^^^^^^^^^^^

The following fields in a product can be either a value, or null:

* variety: text or empty string
* alt_name: text or empty string
* origin: text or empty string
* link: valid URL or empty string
* available: boolean or null

Parameters
^^^^^^^^^^

The ``/products/`` endpoint accepts the ``limit=<int>`` parameter, limiting the
number of products returned to the number requested. For instance,
``/products?limit=5`` will limit the number of results returned to 5.

Example: GET /products/
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: javascript

    {
      "error": {
        "error_status": false,
        "error_name": null,
        "error_text": null,
        "error_level": null
      },
      "products": [
        {
          "id": 1,
          "name": "Salmon",
          "variety": "Chinook",
          "alt_name": "Chinook Salmon",
          "description": "Oregon's state fish, the chinook salmon is the largest in the Pacific salmon genus",
          "origin": "",
          "season": "Late March to October",
          "available": true,
          "market_price": "$24.99",
          "link": "http://en.wikipedia.org/wiki/Chinook_salmon",
          "image": "/media/salmon.jpg",
          "story_id": 2,
          "created": "2014-08-08 23:27:05.568395+00:00",
          "modified": "2014-08-08 23:27:05.568395+00:00"
        },
        {
          "id": 2,
          "name": "Tuna",
          "variety": "Albacore",
          "alt_name": "Tuna fish",
          "description": "Albacore tuna is an Oregon classic, and delicious too!",
          "origin": "",
          "season": "June through October",
          "available": null,
          "market_price": "$2.75 per pound",
          "link": "https://www.youtube.com/watch?v=2lspr6Uh_Dk",
          "image": "/media/tuna.jpg",
          "story_id": 1,
          "created": "2014-08-08 23:27:05.568395+00:00",
          "modified": "2014-08-08 23:27:05.568395+00:00"
        },
      ...
      ]
    }

Product details
---------------

The ``/products/<id>`` endpoint returns the same data as ``/products``, but
only for the product specified by id. This is used when the ID of a product is
known, but the details of the product are not -- for instance, getting details
on a product after finding its ID and name through vendor information.

Optional Fields
^^^^^^^^^^^^^^^

The following fields in a product can be either a value, or null:

* variety: text or empty string
* alt_name: text or empty string
* origin: text or empty string
* link: valid URL or empty string
* available: boolean or null

Example: GET /products/2
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: javascript

    {
      "error": {
        "error_status": false,
        "error_name": null,
        "error_text": null,
        "error_level": null
      },
      "id": 2,
      "name": "Tuna",
      "variety": "Albacore",
      "alt_name": "Tuna fish",
      "description": "Albacore tuna is an Oregon classic, and delicious too!",
      "origin": "",
      "season": "June through October",
      "available": null,
      "market_price": "$2.75 per pound",
      "link": "https://www.youtube.com/watch?v=2lspr6Uh_Dk",
      "image": "/media/tuna.jpg",
      "story_id": 1,
      "created": "2014-08-08 23:27:05.568395+00:00",
      "modified": "2014-08-08 23:27:05.568395+00:00"
    }

Vendors listing
----------------

The vendors listing is available at ``/vendors/``. It returns a JSON array
consisting of each of the vendors, and information about them.

.. note:: Coordinates used in the API are standard, decimal degree coordinates. Many results will contain negative coordinates.

Optional Fields
^^^^^^^^^^^^^^^

The following fields in a vendor can be either a value, or null:

* status: boolean or null
* location_description: text or empty string
* phone: valid 10-digit US phone number or null
* website: valid URL or empty string
* email: valid email or empty string

Parameters
^^^^^^^^^^

Limit
"""""

The ``/vendors/`` endpoint accepts the ``limit=<int>`` parameter, limiting the
number of vendors returned to the number requested. For instance,
``/vendors?limit=5`` will limit the number of results returned to 5.

Location
""""""""

It also accepts ``lat=<float>`` and ``long=<float>`` parameters. When these are
provided, the results will be returned sorted by proximity, with the closest
vendor listed first. For instance, ``/vendors?lat=44.618808&long=-124.049905``
will provide results sorted by distance to the Hatfield Marine Science Center
in Newport, OR. If only one of the parameters is provided, it will be ignored.

Proximity
"""""""""

The ``proximity=<int>`` parameter can be used in conjunction
with the ``lat`` and ``long`` parameters. It will restrict the results to those
within the given number of miles. To get a list of vendors within 10 miles of
the Hatfield Marine Science Center, then, the following could  be queried:

``/vendors?lat=44.618808&long=-124.049905&proximity=10``

As it requires the user's location, it will
be ignored if the ``lat`` and ``long`` positions are not also provided.

Example: GET /vendors/
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: javascript

    {
      "error": {
        "error_status": false,
        "error_name": null,
        "error_text": null,
        "error_level": null
      },
      "vendors": [
        {
          "id": 1,
          "name": "Fish Shack",
          "status": true,
          "description": "We sell fish.",
          "lat": 44.622746,
          "long": -124.056278,
          "street": "1900 SW Coast Hwy",
          "city": "Newport",
          "state": "OR",
          "zip": "97365",
          "location_description": "On top of the bridge",
          "contact_name": "Joe Fisherman",
          "phone": 5551234567,
          "website": "http://example.com",
          "email": "joefisherman@example.com",
          "story": 1,
         "ext": {},
          "created": "2014-08-08 23:27:05.568395+00:00",
          "updated": "2014-08-08 23:27:05.568395+00:00",
          "products": [
            {
              "id": 1,
              "name": "Salmon",
              "preparation": "Frozen"
            },
            {
              "id": 2,
              "name": "Tuna",
              "preparation": "Frozen"
            },
            {
              "id": 3,
              "name": "Clams",
              "preparation": "Frozen"
            }
          ]
        },
        {
          "id": 2,
          "name": "Nullfield Fishery",
          "status": null,
          "description": "All optional fields are blank",
          "lat": 43.423949,
          "long": -124.222432,
          "street": "18632 Oregon Coast Hwy",
          "city": "North Bend",
          "state": "OR",
          "zip": "97459",
          "location_description": "",
          "contact_name": "Hex Fisher",
          "phone": null,
          "website": "",
          "email": "",
          "story": null,
          "ext": {},
          "created": "2014-08-08 23:27:05.568395+00:00",
          "updated": "2014-08-08 23:27:05.568395+00:00",
          "products": [
            {
              "id": 1,
              "name": "Salmon",
              "preparation": "Live"
            }
          ]
        },
        ...
      ]
    }

Vendors selling a product
-------------------------

If a user wants to know which vendors are selling a given product, the
``/vendors/products/<id>`` endpoint should be used. This endpoint returns
a list of all vendors selling the product given by the ID in the same format
as the ``/vendors/`` endpoint. 

Optional Fields
^^^^^^^^^^^^^^^

The following fields in a vendor can be either a value, or null:

* status: boolean or null
* location_description: text or empty string
* phone: valid 10-digit US phone number or null
* website: valid URL or empty string
* email: valid email or empty string

Parameters
^^^^^^^^^^

Limit
"""""

The ``/vendors/products`` endpoint accepts the ``limit`` parameter, limiting
the number of vendors returned to the number requested. For instance,
``/vendors/products/3?limit=5`` will limit the number of results returned to 5.

Location
""""""""

It also accepts ``lat=<float>`` and ``long=<float>`` parameters. When these are
provided, the results will be returned sorted by proximity, with the closest
vendor listed first. For instance, ``/vendors/products/3?lat=44.618808&long=-124.049905``
will provide results sorted by distance to the Hatfield Marine Science Center
in Newport, OR. If only one of the parameters is provided, it will be ignored.

Proximity
"""""""""

The ``proximity=<int>`` parameter can be used in conjunction
with the ``lat`` and ``long`` parameters. It will restrict the results to those
within the given number of miles. To get a list of vendors selling the product
with ID #3 within 10 miles of the Hatfield Marine Science Center, the
following could  be queried:

``/vendors/products/3?lat=44.618808&long=-124.049905&proximity=10``

As it requires the user's location, it will
be ignored if the ``lat`` and ``long`` positions are not also provided.

Example: GET /vendors/products/3
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: javascript

    {
      "error": {
        "error_status": false,
        "error_name": null,
        "error_text": null,
        "error_level": null
      },
      "vendors": [
        {
          "id": 1,
          "name": "Fish Shack",
          "status": true,
          "description": "We sell fish.",
          "lat": 44.622746,
          "long": -124.056278,
          "street": "1900 SW Coast Hwy",
          "city": "Newport",
          "state": "OR",
          "zip": "97365",
          "location_description": "On top of the bridge",
          "contact_name": "Joe Fisherman",
          "phone": 5551234567,
          "website": "http://example.com",
          "email": "joefisherman@example.com",
          "story": 1,
          "ext": {},
          "created": "2014-08-08 23:27:05.568395+00:00",
          "updated": "2014-08-08 23:27:05.568395+00:00",
          "products": [
            {
              "id": 1,
              "name": "Salmon",
              "preparation": "Frozen"
            },
            {
              "id": 2,
            "name": "Tuna",
            "preparation": "Frozen"
            },
            {
              "id": 3,
              "name": "Clams",
              "preparation": "Frozen"
            }
          ]
        },
        {
          "id": 3,
          "name": "Vendor the Third",
          "status": null,
          "description": "Coming in 3rd since 1998",
          "lat": 44.432156,
          "long": -124.070720,
          "street": "1330 NW Pacific Coast Hwy",
          "city": "Waldport",
          "state": "OR",
          "zip": "97394",
          "location_description": "",
          "contact_name": "Ana Ther",
          "phone": null,
          "website": "",
          "email": "",
          "story": null,
          "ext": {},
          "created": "2014-08-08 23:27:05.568395+00:00",
          "updated": "2014-08-08 23:27:05.568395+00:00",
          "products": [
            {
              "id": 3,
              "name": "Clams",
              "preparation": "Live"
            }
          ]
        }
      ]
    }

Vendor details
---------------

The ``/vendors/<id>`` endpoint returns the same data as ``/vendors``, but
only for the vendor specified by id. This is used when the ID of a vendor is
known, but the details of the vendor are not -- for instance, getting details
on a vendor after finding its ID and name through the vendors-for-product list.

Optional Fields
^^^^^^^^^^^^^^^

The following fields in a vendor can be either a value, or null:

* status: boolean or null
* location_description: text or empty string
* phone: valid 10-digit US phone number or null
* website: valid URL or empty string
* email: valid email or empty string

Example: GET /vendors/2
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: javascript

    {
      "error": {
        "error_status": false,
        "error_name": null,
        "error_text": null,
        "error_level": null
      },
      "id": 2,
      "name": "Nullfield Fishery",
      "status": null,
      "description": "All optional fields are blank",
      "lat": 43.423949,
      "long": -124.222432,
      "street": "18632 Oregon Coast Hwy",
      "city": "North Bend",
      "state": "OR",
      "zip": "97459",
      "location_description": "",
      "contact_name": "Hex Fisher",
      "phone": null,
      "website": "",
      "email": "",
      "story": null,
      "ext": {},
      "created": "2014-08-08 23:27:05.568395+00:00",
      "updated": "2014-08-08 23:27:05.568395+00:00",
      "products": [
         {
          "id": 1,
          "name": "Salmon",
          "preparation": "Live"
        }
      ]
    }

Story details
---------------

The ``/stories/<id>`` endpoint returns the story for a given ID.

Example: GET /stories/2
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: javascript

    {
      "error": {
        "error_status": false,
        "error_name": null,
        "error_text": null,
        "error_level": null
      },
      "story": "A story can contain various bits of text."
    }

Preparation details
-------------------

The ``/preparations/<id>`` endpoint returns the preparation details for
a given preparation ID.

Example: GET /preparations/1
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: javascript

    {
      "error": {
        "error_status": false,
        "error_name": null,
        "error_text": null,
        "error_level": null
      },
      "id": 1,
      "name": "Frozen",
      "description": "Fish is generally cooled and frozen as quickly as possible after catching to preserve the meat.",
      "additional_info": "Be sure to ask the fisherman how quickly the fish was cooled after being caught. It is important to get the fish on ice as soon as possible."
    }
