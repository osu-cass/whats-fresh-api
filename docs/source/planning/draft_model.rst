Draft Data model
================

products
--------

.. code-block:: python

    id                          int (pk)
	specific_variety            varchar
	product_name                varchar (optional)
	alt_name                    varchar (optional)
	description                 text
	origin                      varchar? (optional)
	season                      varchar (string describing season?)
	available                   bool (optional, is or is not available now?)
	market_price                varchar
	link                        url (optional, link to industry info site)
	image_id                    int (optional, image foreign key)
	stories_id                  int (optional, image foreign key)
	created                     datetime
	modified                    datetime (auto-update on modification)


vendors
-------

.. code-block:: python

	id                      int (pk)
	name                    varchar
	status                  bool (optional, in or out)
	description             text
	lat                     float
	long                    float
	street                  varchar
	city                    varchar
	state                   varchar
	zip                     varchar
	location_description    text (optional)
	contact_name            varchar
	phone                   varchar (optional)
	website                 url (optional)
	email                   email (optional)
	stories_id              int (optional, story foreign key)
	created                 datetime
	updated                 datetime (auto-update on modification)


stories
-------

.. code-block:: python

	id          int (pk)
    name        varchar
    history     text
    facts       text
    buying      text
    preparing   text
    products    text
    season      text
	created     datetime
	updated     datetime (auto-update on modification)


images
------

.. code-block:: python

	id          int (pk)
	image       image (file)
	caption     text (optional)
	name  	    text
	created     datetime
	updated     datetime (auto-update on modification)


videos
------

.. code-block:: python

	id          int (pk)
	video       url
	name       text
	caption     text (optional)
	created     datetime
	updated     datetime (auto-update on modification)

preparations
------------

.. code-block:: python

	id                  int (pk)
	name                varchar
	description         text (optional)
	additional_info     text (optional)

products_preparations
---------------------

.. code-block:: python

	product_id          int (foreign key to product)
	preparation_id      int (foreign key to preparation)


vendors_products
----------------

.. code-block:: python

	vendors_id           int (vendors foreign key)
	products_id          int (products foreign key)
	preparation_id       int (preparation foreign key)
	vendor_price         varchar (optional)
	available            bool (optional, has this product right now?)
