import requests
import json

from django.contrib.auth.decorators import user_passes_test


class BadAddressException(Exception):
    pass


def get_coordinates_from_address(street, city, state, zip):
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
    def in_groups(u):
        if u.is_authenticated():
            if u.is_superuser | bool(u.groups.filter(name__in=group_names)):
                return True
        return false
    return user_passes_test(in_groups, login_url='/login')
