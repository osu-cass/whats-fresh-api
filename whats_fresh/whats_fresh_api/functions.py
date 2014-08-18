import requests
import json

def get_coordinates_from_address(street, city, state, zip):
    full_address = street + ", " + city + ", " + state + " " + zip
    google_geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json?address="
    print google_geocoding_url + full_address

    response = requests.get(google_geocoding_url + full_address)
    location_data = response.json()

    lat = float(location_data['results'][0]['geometry']['location']['lat'])
    long = float(location_data['results'][0]['geometry']['location']['lng'])
    
    return [lat, long]
