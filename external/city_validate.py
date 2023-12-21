import os

from smartystreets_python_sdk import SharedCredentials, StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_zipcode import Lookup as ZIPCodeLookup


def city_validate(input_city, input_state):
    # auth_id = "53bc7989-9b73-e0a2-7f17-0474a40eb357"
    # auth_token = "EZ7DohIr1axHmw8ZUQkd"

    auth_id = os.environ['SMARTY_AUTH_WEB']
    auth_token = os.environ['SMARTY_WEBSITE_DOMAIN']

    credentials = StaticCredentials(auth_id, auth_token)

    client = ClientBuilder(credentials).build_us_zipcode_api_client()

    lookup = ZIPCodeLookup()
#     lookup.input_id = "dfc33cb6-829e-4fea-aa1b-b6d6580f0817"  # Optional ID from your system
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
