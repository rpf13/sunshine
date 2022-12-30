import random
import geopy
from geopy.geocoders import Nominatim
from classes import MeteoDataCall
import emoji
import re


def validate_input(string):
    """
    Validate the input string to match all possible characters
    available in common town and country names.
    """
    for c in string:
        if not c.isalpha() and c not in [' ', '-', '.', "'", '\u2019']:
            return False
    return True


def validate_address():
    """
    Validate the input address in order to not stress the geopy
    api with wrong searches for impossible places.
    If input is invalid, report and prompt for correct input.
    """
    while True:
        address = input(
            "For which town you want to get the weather? \n"
        ).lower().strip()
        if validate_input(address):
            return address
        else:
            print(f"{address} is not valid, try again!")


def validate_country():
    """
    Validate the input country in order to not stress the geopy
    api with wrong searches for impossible countries.
    If input is invalid, report and prompt for correct input.
    """
    while True:
        country = input(
            "In which country is your town? \n"
        ).lower().strip()
        if validate_input(country):
            return country
        else:
            print(f"{country} is not valid, try again!")


def validate_zip_input(string):
    """
    Validate the input string to match all possible characters
    available in common zip, postalcodes.
    """
    for c in string:
        if not c.isalnum() and c not in [' ', '-']:
            return False
    return True


def validate_postalcode():
    """
    Validate the input zip/postal code to not stress the geopy
    api with wrong searches for impossible countries.
    """
    while True:
        postalcode = input(
            "What is the zip / postal code of your town? \n"
        ).rstrip()
        if validate_zip_input(postalcode):
            return postalcode
        else:
            print(f"{postalcode} is not valid, try again!")


def get_location():
    """
    This function is used to get the latitude/longitude of a specific town,
    to use for API call. User gets prompted to input a town.
    """

    # get the address by calling function
    # which validates user input
    address = validate_address()

    # Initiate the geopy module using Nominatim (OSM)
    # and the geocode for a requested address
    geolocator = Nominatim(user_agent="SUNSHINE")
    location = geolocator.geocode(address)

    # Try / Except block to check for AttributeErrors of user input
    try:
        print(f"You're interested to get the weather for {location.address}.")
    except AttributeError:
        print("This place does not seem to exist!")
        return

    # Ask user to confirm if town fetched via geopy is correct. If not
    # ask for country. Validate also user input (Y or N)

    confirm = input("Can you confirm? Y/N \n").upper().strip()
    while confirm != "Y" and confirm != "N":
        confirm = input("Type either Y or N! \n").upper().strip()
    if confirm == "Y":
        pass
    elif confirm == "N":
        # get the country by calling function
        # which validates user input
        country = validate_country()
        location = geolocator.geocode(f"{address}, {country}")

        # Check if country input is valid. If not, geopy will return None
        if location is not None:
            print(f"You're interested to get the weather for {location}.")
        else:
            print("This place does not seem to exist!")
            return
        
        # Ask user again to confirm if town / country fetched via geopy is
        # correct. If not ask for ZIP code. Validate also user input (Y or N)
        confirm = input("Can you confirm? Y/N \n").upper().strip()
        while confirm != "Y" and confirm != "N":
            confirm = input("Type either Y or N! \n").upper().strip()
        if confirm == "Y":
            pass
        elif confirm == "N":

            # get postalcode by calling function
            # which validates user input
            postalcode = validate_postalcode()
            
            # important to not include city in search, only country and
            # postalcode, otherwise wrong positives will appear
            location = geolocator.geocode(f"{country}, {postalcode}")

            # Check if postalcode input is valid. If not,
            # geopy will return None
            if location is not None:
                print(
                    "You're interested to get the weather for "
                    f"{postalcode}, {address}, {country}."
                )
            else:
                print("This place does not seem to exist!")
                return
    coordinates = [location.latitude, location.longitude]
    return coordinates


# Create a weather-report based on the received WMO Weather
# interpretation weathercode using the translation table on
# open-meteo.com api reference.
def translate_weathercode():
    """
    Function to translate the weathercode into a human readable code
    and assign ascii art element to it.
    """
    weathercode = weatherdata["current_weather"]["weathercode"]
    if weathercode == 0:
        weathercondition = "clear skies"
    elif weathercode == 1:
        weathercondition = "mainly clear"
    elif weathercode == 2:
        weathercondition = "partly cloudy"
    elif weathercode == 3:
        weathercondition = "overcast"
    elif weathercode == 45 or weathercode == 48:
        weathercondition = "foggy"
    elif weathercode == 51:
        weathercondition = "light drizzle"
    elif weathercode == 53:
        weathercondition = "moderate drizzle"
    elif weathercode == 55:
        weathercondition = "dense drizzle"
    elif weathercode == 56 or weathercode == 57:
        weathercondition = "light freezing drizzle"
    elif weathercode == 57:
        weathercondition = "dense freezing drizzle"
    elif weathercode == 61:
        weathercondition = "slight rain"
    elif weathercode == 63:
        weathercondition = "moderate rain"
    elif weathercode == 65:
        weathercondition = "heavy rain"
    elif weathercode == 66:
        weathercondition = "light freezing rain"
    elif weathercode == 67:
        weathercondition = "heavy freezing rain"
    elif weathercode == 71:
        weathercondition = "slight snow"
    elif weathercode == 73:
        weathercondition = "moderate snow"
    elif weathercode == 75 or weathercode == 77:
        weathercondition = "heavy snow"
    elif weathercode == 80:
        weathercondition = "slight rain showers"
    elif weathercode == 81:
        weathercondition = "moderate rain showers"
    elif weathercode == 82:
        weathercondition = "violent rain showers"
    elif weathercode == 85:
        weathercondition = "slight snow showers"
    elif weathercode == 86:
        weathercondition = "heavy snow showers"
    elif weathercode == 95:
        weathercondition = "thunderstorms"
    elif weathercode == 96 or weathercode == 99:
        weathercondition = "thunderstorms with hail"
    else:
        weathercondition = "none"
    return weathercondition

# ====---- Remember to reactivate the geodata geopy function ===---

# coordinates = get_location()
# print(coordinates)


coordinates = [46.2017559, 6.1466014]
# coordinates = ['ada', 'beda']

api_fetcher = MeteoDataCall(coordinates)
weatherdata = api_fetcher.live_data()
if weatherdata is not None:
    print(weatherdata)
    print(weatherdata["current_weather"]["weathercode"])
else:
    print("An error occurred while fetching the data.")

weathercondition = translate_weathercode()
print(f"the condition at this location is {weathercondition}")

# print(
#     "The weather at this location is "
#     f"{weathercondition} "
#     f"{emoji.CONDITIONS[weathercondition.replace(' ', '_')]}"
# )
