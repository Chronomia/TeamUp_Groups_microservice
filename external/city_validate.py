import os

from smartystreets_python_sdk import SharedCredentials, StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_zipcode import Lookup as ZIPCodeLookup


def city_validate(input_city, input_state):
    auth_id = os.environ['SMARTY_AUTH_WEB']
    auth_token = os.environ['SMARTY_WEBSITE_DOMAIN']

    credentials = StaticCredentials(auth_id, auth_token)

    client = ClientBuilder(credentials).build_us_zipcode_api_client()

    lookup = ZIPCodeLookup()
    lookup.city = input_city
    lookup.state = input_state
#     lookup.zipcode = "10025"

    try:
        client.send_lookup(lookup)
    except exceptions.SmartyException as err:
        print(err)
        return

    result = lookup.result
    zipcodes = result.zipcodes
    cities = result.cities
    
    return cities
