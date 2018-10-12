import json
import os
import googlemaps
from datetime import datetime


class Geolocation:
    CACHE_PATH = 'data/geocode_cache.json'

    def __init__(self, maps_api_key):
        self.cache = self.load_cache()
        self.client = googlemaps.Client(key=maps_api_key)

    def load_cache(self):
        if not os.path.exists(self.CACHE_PATH):
            return {}

        with open(self.CACHE_PATH, 'r') as f:
            return json.load(f)

    def write_cache(self):
        with open(self.CACHE_PATH, 'w') as f:
            json.dump(self.cache, f)

    def geocode(self, address, ship_cache_write=False):
        cached = self.cache.get(address)
        if cached is not None:
            return cached

        res = self.client.geocode(address)
        self.cache[address] = res
        self.write_cache()

        return res

    def extract_lat(self, address):
        geocoded = self.geocode(address)
        if len(geocoded) == 0:
            print(address)
        return geocoded[0]['geometry']['location']['lat']

    def extract_lng(self, address):
        geocoded = self.geocode(address)
        return geocoded[0]['geometry']['location']['lng']

    def extract_country(self, address):
        geocoded = self.geocode(address)

        for component in geocoded[0]['address_components']:
            if 'country' in component['types']:
                country = component['long_name']
                if country == '' and component['short_name'] == 'CN':
                    return 'China'
                else:
                    return country

    def extract_region(self, address):
        geocoded = self.geocode(address)

        for component in geocoded[0]['address_components']:
            if 'administrative_area_level_1' in component['types']:
                return component['long_name']
