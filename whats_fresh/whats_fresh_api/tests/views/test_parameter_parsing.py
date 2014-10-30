from django.test import TestCase
from whats_fresh.whats_fresh_api.functions import get_lat_long_prox, get_limit
from mock import Mock, patch
from django.contrib.gis.geos import fromstr

class ParameterTestCase(TestCase):
    """
    Test that the parameter parsing functions get_lat_long_prox and get_limit
    work as expected.

    1. get_limit with valid limit
    2. get_limit with invalid limit
    3. get_limit with invalid limit and existing error block

    1. get_lat_long_prox with valid lat, long, and prox
    2. get_lat_long_prox with valid lat, long, no prox
    3. get_lat_long_prox with valid lat, not valid long
    4. get_lat_long_prox with valid lat, no long
    5. get_lat_long_prox with valid lat, long, prox, and limit
    """

    def setUp(self):
        self.base_error = {
            'status': False,
            'level': None,
            'debug': None,
            'text': None,
            'name': None
        }

    @patch('django.http.request')
    def test_get_limit_valid_limit(self, mock_request):
        mock_request = Mock()
        mock_request.GET = {'limit': '80'}

        expected_result = [80, self.base_error]
        actual_result = get_limit(mock_request, self.base_error)

        self.assertEqual(expected_result, actual_result)


    @patch('django.http.request')
    def test_get_limit_invalid_limit(self, mock_request):
        mock_request = Mock()
        mock_request.GET = {'limit': 'I like Pi'}

        expected_error = {
            'debug': "ValueError: invalid literal for int() "
                     "with base 10: 'I like Pi'",
            'status': True,
            'level': 'Warning',
            'text': 'Invalid limit. Returning all results.',
            'name': 'Bad Limit'
        }

        expected_result = [None, expected_error]
        actual_result = get_limit(mock_request, self.base_error)

        self.assertEqual(expected_result, actual_result)


    @patch('django.http.request')
    def test_get_limit_invalid_limit_existing_error(self, mock_request):
        mock_request = Mock()
        mock_request.GET = {'limit': 'I like Pi'}

        original_error = {
            'debug': "This is an existing error",
            'status': True,
            'level': 'Important',
            'text': 'This error already exists',
            'name': "I've errored!"
        }

        expected_error = {
            'debug': "ValueError: invalid literal for int() "
                     "with base 10: 'I like Pi'",
            'status': True,
            'level': 'Warning',
            'text': 'Invalid limit. Returning all results.',
            'name': 'Bad Limit'
        }

        expected_result = [None, expected_error]
        actual_result = get_limit(mock_request, original_error)

        self.assertEqual(expected_result, actual_result)


    @patch('django.http.request')
    def test_get_lat_long_prox_valid_lat_long_prox(self, mock_request):
        mock_request = Mock()
        mock_request.GET = {'lat': '45.6', 'lng': '-123.4', 'proximity': '25'}

        point = fromstr('POINT (-123.4000000000000057 45.6000000000000014)',
            srid=4326)

        expected_result = [point, 25, None, self.base_error]
        actual_result = get_lat_long_prox(mock_request, self.base_error)

        self.assertEqual(expected_result[1:], actual_result[1:])
        self.assertEqual(expected_result[0].x, actual_result[0].x)
        self.assertEqual(expected_result[0].y, actual_result[0].y)


    @patch('django.http.request')
    def test_get_lat_long_prox_valid_lat_long_no_prox(self, mock_request):
        mock_request = Mock()
        mock_request.GET = {'lat': '45.6', 'lng': '-123.4'}

        point = fromstr('POINT (-123.4000000000000057 45.6000000000000014)',
            srid=4326)

        expected_result = [point, 20, None, self.base_error]
        actual_result = get_lat_long_prox(mock_request, self.base_error)

        self.assertEqual(expected_result[1:], actual_result[1:])
        self.assertEqual(expected_result[0].x, actual_result[0].x)
        self.assertEqual(expected_result[0].y, actual_result[0].y)


    @patch('django.http.request')
    def test_get_lat_long_prox_valid_lat_bad_long(self, mock_request):
        mock_request = Mock()
        mock_request.GET = {'lat': '45.6', 'lng': 'kittens'}

        expected_error = {
            "level": "Warning",
            "status": True,
            "name": "Bad location",
            "text": "There was an error with the given "
                     "coordinates 45.6, kittens",
            'debug': "ValueError: String or unicode input unrecognized "
                     "as WKT EWKT, and HEXEWKB."
            }

        expected_result = [None, 20, None, expected_error]
        actual_result = get_lat_long_prox(mock_request, self.base_error)

        self.assertEqual(expected_result, actual_result)


    @patch('django.http.request')
    def test_get_lat_long_prox_valid_lat_no_long(self, mock_request):
        mock_request = Mock()
        mock_request.GET = {'lat': '45.6'}

        expected_error = {
            "level": "Warning",
            "status": True,
            "name": "Bad location",
            "text": "There was an error with the given "
                     "coordinates 45.6, None",
            'debug': 'GEOSException: Error encountered checking Geometry '
                     'returned from GEOS C function "GEOSWKTReader_read_r".'
            }

        expected_result = [None, 20, None, expected_error]
        actual_result = get_lat_long_prox(mock_request, self.base_error)

        self.assertEqual(expected_result, actual_result)


    @patch('django.http.request')
    def test_get_lat_long_prox_valid_lat_long_prox_limit(self, mock_request):
        mock_request = Mock()
        mock_request.GET = {
            'lat': '45.6',
            'lng': '-123.4',
            'proximity': '25',
            'limit': '80'
        }

        point = fromstr('POINT (-123.4000000000000057 45.6000000000000014)',
            srid=4326)

        expected_result = [point, 25, 80, self.base_error]
        actual_result = get_lat_long_prox(mock_request, self.base_error)

        self.assertEqual(expected_result[1:], actual_result[1:])
        self.assertEqual(expected_result[0].x, actual_result[0].x)
        self.assertEqual(expected_result[0].y, actual_result[0].y)
