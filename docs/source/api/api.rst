.. _api:

API Endpoints
=============

The What's Fresh API is a REST-style JSON API for discovering fresh
local food products.

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
        "status": false,
        "text": null,
        "name": null,
        "debug": null,
        "level": null
      },
      "products": [
        {
          "origin": "Pacific Ocean",
          "available": null,
          "description": "A classic fish",
          "variety": "Salmon",
          "season": "July - October",
          "image": null,
          "created": "2014-09-18T18:33:22.140Z",
          "modified": "2014-09-24T19:42:52.720Z",
          "market_price": "$100 per fluid ounce",
          "link": "",
          "alt_name": "Oncorynchus kisutch",
          "story_id": null,
          "id": 1,
          "name": "Coho Salmon"
        },
        {
          "origin": "Pacific Ocean",
          "available": null,
          "description": "A popular seafood prized for its sweet and tender flesh. ",
          "variety": "Dungeness",
          "season": "December to January",
          "image": null,
          "created": "2014-09-18T18:36:14.240Z",
          "modified": "2014-09-24T19:43:08.960Z",
          "market_price": "$0.10 per dozen",
          "link": "",
          "alt_name": "Metacarcinus magister",
          "story_id": null,
          "id": 2,
          "name": "Dungeness Crab"
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
        "status": false,
        "debug": null,
        "text": null,
        "name": null,
        "level": null
      },
      "origin": "Pacific Ocean",
      "available": null,
      "modified": "2014-09-24T19:43:08.960Z",
      "description": "A popular seafood prized for its sweet and tender flesh. ",
      "variety": "Dungeness",
      "season": "December to ???",
      "image": null,
      "created": "2014-09-18T18:36:14.240Z",
      "market_price": "$0.10 per dozen",
      "link": "",
      "alt_name": "Metacarcinus magister",
      "story_id": null,
      "id": 2,
      "name": "Dungeness Crab"
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
* phone: valid phone number (with international prefix) as string or null
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
          "status": null,
          "city": "Newport",
          "website": "",
          "modified": "2014-09-24T19:55:16.085Z",
          "description": "A local tuna provider.",
          "zip": "97365",
          "created": "2014-09-23T23:52:51.484Z",
          "story_id": 1,
          "ext": {
          },
          "location_description": "",
          "email": "",
          "hours": "",
          "phone": null,
          "state": "Oregon",
          "street": "1398 SW Bay St",
          "products": [
            {
              "preparation": "Filet",
              "preparation_id": 3,
              "product_id": 3,
              "name": "Albacore Tuna"
            }
          ],
          "lng": 44.6266099,
          "lat": -124.0565731,
          "contact_name": "Todd Sherman",
          "id": 2,
          "name": "Todd's Tuna Farm"
        },
        {
          "status": true,
          "city": "Gold Beach",
          "website": "",
          "modified": "2014-09-24T20:49:33.156Z",
          "description": "Best shark meat in the west.",
          "zip": "97444",
          "created": "2014-09-23T23:59:20.016Z",
          "story_id": 1,
          "ext": {
          },
          "location_description": "",
          "email": "",
          "hours": "",
          "phone": null,
          "state": "Oregon",
          "street": "29985 Harbor Way",
          "products": [
            {
              "preparation": "Live",
              "preparation_id": 1,
              "product_id": 5,
              "name": "Leopard Shark"
            }
          ],
          "lng": 42.4210811,
          "lat": -124.4179554,
          "contact_name": "James Renolds",
          "id": 3,
          "name": "The Shark Shop"
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
* phone: valid phone number (with international prefix) as string or null
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
    {
      "vendors": [
        {
          "status": null,
          "city": "Newport",
          "website": "",
          "modified": "2014-09-24T19:55:16.085Z",
          "description": "A local tuna provider.",
          "zip": "97365",
          "created": "2014-09-23T23:52:51.484Z",
          "story_id": 1,
          "ext": {
          },
          "location_description": "",
          "email": "",
          "hours": "",
          "phone": null,
          "state": "Oregon",
          "street": "1398 SW Bay St",
          "products": [
            {
              "preparation": "Filet",
              "preparation_id": 3,
              "product_id": 3,
              "name": "Albacore Tuna"
            }
          ],
          "lng": 44.6266099,
          "lat": -124.0565731,
          "contact_name": "Todd Sherman",
          "id": 2,
          "name": "Todd's Tuna Farm"
        },
        {
          "status": null,
          "city": "Waldport",
          "website": "",
          "modified": "2014-09-24T20:50:37.652Z",
          "description": "The freshest seafood in Waldport.",
          "zip": "97394",
          "created": "2014-09-24T00:06:43.426Z",
          "story_id": 1,
          "ext": {
          },
          "location_description": "",
          "email": "",
          "hours": "",
          "phone": null,
          "state": "Oregon",
          "street": "98 NW Alsea Bay Dr",
          "products": [
            {
              "preparation": "Live",
              "preparation_id": 1,
              "product_id": 7,
              "name": "Savory Clam"
            },
            {
              "preparation": "Filet",
              "preparation_id": 3,
              "product_id": 3,
              "name": "Albacore Tuna"
            }
          ],
          "lng": 44.4269468,
          "lat": -124.0792542,
          "contact_name": "Carlos Molena",
          "id": 4,
          "name": "Waterfront Seafood Shop"
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
* phone: valid phone number (with international prefix) as string or null
* website: valid URL or empty string
* email: valid email or empty string

Example: GET /vendors/2
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: javascript

    {
      "error": {
        "debug": null,
        "status": false,
        "text": null,
        "name": null,
        "level": null
      },
      "website": "",
      "street": "1398 SW Bay St",
      "lng": 44.6266099,
      "contact_name": "Todd Sherman",
      "city": "Newport",
      "zip": "97365",
      "story_id": 1,
      "location_description": "",
      "id": 2,
      "state": "Oregon",
      "email": "",
      "status": null,
      "modified": "2014-08-08T23:27:05.568Z",
      "description": "A local tuna provider.",
      "hours": "",
      "phone": null,
      "lat": -124.0565731,
      "name": "Todd's Tuna Farm",
      "created": "2014-08-08T23:27:05.568Z",
      "ext": {
      },
      "products": [
        {
          "preparation": "Filet",
          "preparation_id": 3,
          "product_id": 3,
          "name": "Albacore Tuna"
        }
      ]
    }

Story details
---------------

The ``/stories/<id>`` endpoint returns the same data as ``/stories``, but
only for the story specified by id. This is used when the ID of a vendor is
known, but the details of the story are not.

Optional Fields
^^^^^^^^^^^^^^^

The following fields in a vendor can be either a value, or null:

* images: this field may be an empty list
* videos: this field may be an empty list

Any of the text fields may be empty strings.

Example: GET /stories/2
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: javascript

    {
        "error": {
            "status": false,
            "text": null,
            "name": null,
            "debug": null,
            "level": null
        },
        "name": "Tuna",
        "videos": [
            {
                "caption": "A video all about tuna",
                "link": "https://www.youtube.com/watch?v=Awf45u6zrP0",
                "name": "Tuna! They rock!"
            }
        ],
        "created": "2014-08-08T23:27:05.568Z",
        "season": "Tuna can be harvested between Jultember and Januly.",
        "modified": "2014-12-04T18:31:27.319Z",
        "facts": "Tuna are a fish that can be eaten. Great in salads!",
        "ext": { },
        "products": "Canned tuna fish is pretty common.",
        "preparing": "Boil 'em, mash 'em, stick 'em in a stew",

        "images": [
            {
                "caption": "Tuna photo!",
                "link": "/media/images/tuna-fighting-catfish.jpg",
                "name": "Tuna Picture"
            },
            {
                "caption": "This is a tuna fish.",
                "link": "/media/images/tuna.jpg",
                "name": "Tuna Picture 2"
            }
        ],
        "id": 2,
        "buying": "To buy a tuna just head down to the docks.",
        "history": "Tuna have been eaten for years and years."

    }



Preparation details
-------------------

The ``/preparations/<id>`` endpoint returns the preparation details for
a given preparation ID.

Example: GET /preparations/4
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: javascript

    {
      "error": {
        "status": false,
        "debug": null,
        "text": null,
        "name": null,
        "level": null
      },
      "name": "Smoked",
      "description": "Thats dense stuff, tastes like forest fire.",
      "additional_info": "",
      "id": 4
    }

Locations list
--------------

The ``/locations/`` endpoint returns a list of all the cities this vendors
are in. Each city is given an location index, and a name. The index is not
guaranteed to stay the same.

Example: GET /locations/
^^^^^

.. code-block:: javascript

    {
      "error": {
        "status": false,
        "name": null,
        "text": null,
        "debug": null,
        "level": null
      },
      "locations": [
        {
          "location": 1,
          "name": "Gold Beach"
        },
        {
          "location": 2,
          "name": "Corvallis"
        },
        {
          "location": 3,
          "name": "Florence"
        },
        {
          "location": 4,
          "name": "Newport"
        }
      ]
    }