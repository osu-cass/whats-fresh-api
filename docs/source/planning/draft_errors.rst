Draft Error Handling
====================

Proposal for error types and levels to be returned by API endpoints

The error array
---------------


.. code-block:: json

    error:     {
        status: true, 
        name: 'name_of_error',
        text: 'end-user friendly error message',
        level: 'error_level'
        debug: 'detailed debug info'
    }


Error Levels
------------

**Information**
Additional information (deprecation warning?) is available, otherwise API response is complete and correct. Information type errors should return a 200 response.

**Warning** 
A warning about the state of the database or data contained is available, API response is complete, but may be incorrect, or is correct but may be incomplete. A known error occurred, which is reported in the error text. Warnings will most likely return a 400 response.

**Error**
Some fatal error has occurred on the API back end, and no API response can be returned, other than the error array. Errors should  return a 404 or 500 response.

Error status will be true for any error level, consumer code should check both the status and level to determine the appropriate action.


Error names and messages
------------------------
 
(this list will expand as we discover new ways to break things)

**Object Not Found**

(single object)
    "<object> id <requested_id> was not found."
    (ex: Vendor id 237 was not found)

(list)
    "No <object>s were found."
    (ex: No Vendors were found)

**Malformed/bad parameter**

(location)
    "There was an error with the given coordinates <lat, long>"
    debug message: "<error returned by geodjango>"

    (this can be changed as we implement move form validation and catch the error before geodjango does. This can be a Warning error, as we can return some default set of data, but it won’t be what the client really wanted. It may also be a 404 error, we need to determine whether to return a default data set, or nothing.)

(proximity)
    "Proximity <proximity> is out of range. Falling back to default <default proximity>"
    "Proximity <proximity> is malformed.  Falling back to default <default proximity>"

    (depending on the actual issue - this is a good example of the Information error level, as we default to 20 miles if the parameter is missing or bad)

(limit)
    "Limit <limit> is out of range. Returning all results."
    "Limit <limit> is malformed. Returning all results."
    (depending on the actual issue - this is a good example of the Information error level, as we default to ignoring the limit if it is malformed.)


HTTP Response codes
-------------------

Responses containing specific types of errors will report an appropriate HTTP response code as well as the error array containing information about the error.

Malformed parameters: 400
    Ex. coordinates given are in the wrong format

Object Not Found: 404
    Ex. can’t find the vendor or product requested

Code or query execution error: 500
    Ex. we have an error in the code that raised an exception

An empty list of objects will return a 200 code.
