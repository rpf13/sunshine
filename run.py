# Write your code to expect a terminal of 80 characters wide and 24 rows high

import random
import geopy
from geopy.geocoders import Nominatim
import requests
from classes import MeteoDataCall



def get_location():
    """
    This function is used to get the latitude/longtitude of a specific town,
    to use for API call. User gets prompted to input a town.
    """
    address = (input("For which town you want to get the weather? ").lower().strip())

    # Initiate the geopy module using Nominatim (OSM) and the geocode for a address
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
        country = (input("In which country is your town? \n").lower().strip())
        location = geolocator.geocode(f"{address}, {country}")

        # Check if country input is valid. If not, geopy will return None
        if location != None:
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
            postalcode = input("What is the zip code of your town? \n").rstrip()
            
            # important to not include city in search, only country and postalcode,
            # otherwise wrong positives will appear
            location = geolocator.geocode(f"{country}, {postalcode}")

            # Check if postalcode input is valid. If not, geopy will return None
            if location != None:
                print(f"You're interested to get the weather for {postalcode}, {address}, {country}.")
            else:
                print("This place does not seem to exist!")
                return
    coordinates = [location.latitude, location.longitude]
    return coordinates

# coordinates = get_location()
# 
# print(coordinates)

coordinates = [46.2017559, 6.1466014]

api_fetcher = MeteoDataCall(coordinates)
weatherdata = api_fetcher.live_data()
if weatherdata:
    print(weatherdata)
else:
    print("An error occurred while fetching the data.")

