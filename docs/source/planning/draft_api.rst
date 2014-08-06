Draft API
=========

Format
------

Responses will be returned in standard JSON format. An attempt will be made to keep the structure simple. Https will be used for all endpoints. 

Null values (optional fields that do not have data), will be empty strings: "".

Versions
--------

The API will be versioned with simple version integers, 1, 2, 3, ...

ex: https://whatsfresh.org/1/vendors

Errors
------

Error records will be returned in every message, and will consist of a dictionary containing the error status, error name, error text and error level. The status field will indicate the presence of an error condition, and should be checked before attempting to process the rest of the response.

example:

.. code-block:: json

	error: {error_status: true, error_name: 'not_found_error', error_text: 'product with id=232 could not be found', error_level: 10}

Extended Fields
---------------

To allow for future expandability, a dictionary call 'ext' will be included with every response. This dictionary will either contain no records, or will contain additional first-class records that were not included in the original specification. For instance, if a new attribute "color" is later added to the product response, it can be included in the extended attributes array. Applications can choose to discover/use these new fields or ignore them without effecting backwards compatibility. Response validation should include the presence of ext, but not its contents.


Endpoints
---------

*/products*

Return a dictionary containing a record for every product in the database.The product id is the record key. This data is unlikely to change frequently, it should be in long-term storage on the device and refreshed periodically.

.. code-block:: json

	{
		error: {error_status: bool, error_name: text, error_text: text, error_level},
	    <product_id>: { 
			name: text
			variety: text or null
			alt_name: text or null
			description: text
			origin: text or null
			season: text
			available: bool or null
			market_price: text
			preparations: [smoked, fresh, live...]
			link: url or null
			image: int or null
			story: int or null
			created: datetime
			modified: datetime
			ext: {attribute: value, attribute: value...} or {}	
		},
		<product_id>: {...},
		...
	}


*/products/<id>*

Returns a single product record identified by <id>. This may be useful for selectively refreshing the local master list of products fetched by /products.

.. code-block:: json

	{
		error: {error_status: bool, error_name: text, error_text: text, error_level},
		id: int
		name: text
		variety: text or null
		alt_name: text or null
		description: text
		origin: text or null
		season: text
		available: bool or null
		bool: bool
		market_price: text
		preparations: [text, text, text...]
		link: url or null
		image: int or null
		story: int or null
		created: datetime
		modified: datetime
		ext: {attribute: value, attribute: value...}			
	}
	

*/products/describe*

Returns a description of the fields in a product record. These should correspond to internal docstrings, which in turn should be extracted into the master project documentation.

.. code-block:: json

	{
		endpoint_description: "text describing the endpoint"
		id: "text describing this field"
		name: "text describing this field"
		...
	}


*/vendors*

Return a dictionary containing a record for each vendor in the database. The vendor id is the record key. Each vendor record also contains a dictionary of products carried by this vendor. This data is likely to change more often, and should be cached locally but refreshed for specific products or locations whenever possible.

.. code-block:: json

	{
		error: {error_status: bool, error_name: text, error_text: text, error_level},
		<vendor_id>: {
			name: text
			status: bool or null
			description: text
			lat: float
			long float
			street: text
			city: text
			state: text
			zip: text
			location_description: text or null
			contact_name: text
			phone: text or null
			website: url or null
			email: email or null
			story: int or null
			ext: {attribute: value, attribute: value...}
			created: datetime
			updated: datetime
			products: {
				<product_id>: {name: text, preparation: text},
				<product_id>: {name: text, preparation: text},...
			}
		},
		<vendor_id>: {...},
		...
	}


*/vendors/<id>*

Returns a single vendor record identified by <id>. This should be used to fetch data whenever a specific vendor id is known.

.. code-block:: json

	{
		id: int
		name: text
		status: bool or null
		description: text
		gps_location: coords
		street: text
		city: text
		state: text
		zip: text
		location_description: text
		contact_name: text
		phone: text or null
		website: url or null
		email: email or null
		story: int or null
		ext: {attribute: value, attribute: value...}
		created: datetime
		updated: datetime			
		products: {
			<product_id>: {name: text, preparation: text},
			<product_id>: {name: text, preparation: text},...
		}
	}


*/vendors/describe*

Returns a description of the fields in a vendor record. These should correspond to internal docstrings, which in turn should be extracted into the master project documentation.

.. code-block:: json

	{
		id: (text describing this field)
		...
	}


*/stories/<id>*

Returns a story record identified by <id>.

.. code-block:: json

	{
		story: "text"
	}


*/images/<id>*

Returns an image record identified by <id>. Alternatively, this could return the image data itself as content-type image rather than json.

.. code-block:: json

	{
		image: "url to image"
		caption: "text" or null
	}


*/vendors/product/<id>*

Returns a dictionary of vendors that carry a product identified by <id>. The records are identical to those returned by /vendors/<id>, but filtered by the product id.


*/nearby/?lat=<float>&long=<float>*

Returns nearby available vendors. Vendor records are as defined above, including the products array.



Additional parameters
---------------------

These parameters can be added to any endpoint request

*?location=<lat>,<long>*

or 

*?lat=<float>&long=<float>*

These parameters represent the latitude and longitude of either the mobile device’s current location, or a pre-defined location such as “Newport, OR”. These will cause the results to be sorted by proximity, closest items first. This parameter will be ignored with the /stories endpoint. Depending on how the device handles the coordinates, it may be more convenient to send a single parameter, ‘location=<lat>,<long>’ and use the latitude and longitude as positional arguments.

examples:

.. raw:: html

	https://whatsfresh.org/vendors?lat=49.28472&long=89.7982
	https://whatsfresh.org/vendors?location=49.28472,89.7982


*?limit=<int>*

This parameter will limit the number of records returned to <int>. In combination with the location parameter, it can be used to return the 5 nearest vendors selling tuna:

.. raw:: html

	https://whatsfresh.org/vendors/product/<tuna_id>?lat=49.28472&long=89.7982

*?proximity=<int>*

This parameter will restrict the returned results to those within <int> miles (or configurable distance unit) of the given location. Ignored if no location is given.
