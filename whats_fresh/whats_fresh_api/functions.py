import requests
import json

from django.contrib.auth.decorators import user_passes_test


class BadAddressException(Exception):
    """
    The exception thrown if the address passed in invalid.
    """
    pass


def get_coordinates_from_address(street, city, state, zip):
    """
    This function returns a list of the coordinates from the address
    passed using the Google Geocoding API. If the address given does not
    return an exact coordinates (for instance, if the address can only be
    located down to the city), a BadAddressException is thrown.

    TODO: this should probably return a tuple, rather than a list.
    """
    try:
        full_address = street + ", " + city + ", " + state + " " + zip
        google_geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json?address="

        response = requests.get(google_geocoding_url + full_address)
        location_data = response.json()

        if location_data['results'][0][
                'geometry']['location_type'] == 'APPROXIMATE':
            raise BadAddressException("Address %s not found" % full_address)

        lat = float(location_data['results'][0]['geometry']['location']['lat'])
        long = float(
            location_data['results'][0]['geometry']['location']['lng'])

        return [lat, long]
    except:
        raise BadAddressException("Address %s not found" % full_address)

def group_required(*group_names):
    """
    This decorator can be used to protect a view from users not in a given list
    of groups. Add @group_required to a view to require the user to be logged
    in and part of the passed groups. If the user is not a member of the given
    groups, they will be redirected to /login.
    """
    def in_groups(u):
        if u.is_authenticated():
            if u.is_superuser | bool(u.groups.filter(name__in=group_names)):
                return True
        return False
    return user_passes_test(in_groups, login_url='/login')
