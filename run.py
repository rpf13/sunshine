import random
import geopy
from geopy.geocoders import Nominatim
from classes import MeteoDataCall
import my_emoji
import os
import pyfiglet
import time
import sys
import re


# Some generic "global" functions used on various places

def clear_screen():
    """
    Clear screen function to clean up the terminal
    """
    os.system("cls" if os.name == "nt" else "clear")


# Some functions follow, which validate user input required
# to get the geodata from OSM (Open Street Map) for a specific place
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


# Function to get geodata from geopy module (api)
def get_location():
    """
    This function is used to get the latitude/longitude of a specific town,
    required for the open-meteo api call. User gets prompted to input a town,
    country or postal code. The input is used to get the data via the OSM
    Nominatim module, which is basically an api call. Return value is an
    array with the latitude, longitude value.
    """
    clear_screen()
    # get the address by calling function
    # which validates user input
    address = validate_address()

    # Initiate the geopy module using Nominatim (OSM)
    # and the geocode for a requested address
    geolocator = Nominatim(user_agent="SUNSHINE")
    # try / except block to handle geopy api errors
    try:
        location = geolocator.geocode(address)
    except GeocoderUnavailable:
        print("The Geocoder API is currently unavailable")
        return
    except Exception as error:
        print(f"There was an undefined error {error}")
        return

    # Check if country input is valid. If not, geopy will return None
    if location is not None:
        print(
            f"You're interested to get the weather for {location}.")
    else:
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
        # try / except block to handle geopy api errors
        try:
            location = geolocator.geocode(f"{address}, {country}")
        except GeocoderUnavailable:
            print("The Geocoder API is currently unavailable")
            return
        except Exception as error:
            print(f"There was an undefined error {error}")
            return

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

            # try / except block to handle geopy api errors
            # important to not include city in search, only country and
            # postalcode, otherwise wrong positives will appear
            try:
                location = geolocator.geocode(f"{country}, {postalcode}")
            except GeocoderUnavailable:
                print("The Geocoder API is currently unavailable")
                return
            except Exception as error:
                print(f"There was an undefined error {error}")
                return

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


# Translate the weathercode from api call
def translate_weathercode(weatherdata):
    """
    Function to translate the received WMO weathercode into
    a human readable code using the translation table on
    open-meteo.com api reference.
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


# Function to get the live weather from related resources
def get_live_weather():
    """
    This function gets all necessary data for the live weather,
    calls the required functions and classes and prints the
    result to the user. It will enhance the data with related
    emoji's from the my_emoji CONDITIONS hash.
    """
    # ===-- REMEMBER TO REACTIVATE GEOPY FUNCTION W. LINE BELOW===--
    # coordinates = [46.2017559, 6.1466014]
    # Verify if the geopy lookup did return anything, if None, send back
    # to the main menu and report an error
    coordinates = get_location()
    if coordinates is None:
        print(
            "There was an error when calling the Open Streetmap"
            "API Please try again later"
        )
        main()

    # Call the Meteo API Class
    api_fetcher = MeteoDataCall(coordinates)
    weatherdata = api_fetcher.live_data()
    weathercondition = translate_weathercode(weatherdata)
    temperature = weatherdata["current_weather"]["temperature"]
    windspeed = weatherdata["current_weather"]["windspeed"]
    # If weather api call was successful and did not return None
    if weatherdata is not None:
        # Print temperature for desired location
        print(f"The current temperature there is: {temperature} ℃")
        # If there is a valid weathercode and significant windspeed
        if weathercondition != "none" and windspeed > 2:
            print(
                "The weather at this location is "
                f"{weathercondition} "
                f"{my_emoji.CONDITIONS[weathercondition.replace(' ', '_')]}\n"
                f"There is wind with the speed of {windspeed} km/h"
            )
        elif weathercondition != "none" and windspeed <= 2:
            print(
                "The weather at this location is "
                f"{weathercondition} "
                f"{my_emoji.CONDITIONS[weathercondition.replace(' ', '_')]}\n"
                f"There is no wind"
            )
    # if there was an error w. the open-meteo api and hence we got
    # None back from the Class MeteoDataCall
    else:
        print("An error occurred while fetching the data.")


# Loop for live weather function, until user decides to leave
def live_weather_loop():
    """
    This function creates a live_weather loop, asking the user repeatedly
    if he wants to take another live_weather round. If negative, will
    bring the user back to the main menu via calling main().
    """
    while True:
        get_live_weather()
        answer = input(
            "Do you want to get the weather for another location? Y/N \n"
        ).upper().strip()
        if answer == "N":
            main()
            break
        elif answer == "Y":
            continue
        else:
            print("Please input either Y or N.")


# Main function to control the tool, display menu to user
def main():
    """
    This is the main function and the starting point of the tool.
    It will clear the screen and display the menu to the user.
    It will request the user to enter the number for one of the
    given options.
    """
    clear_screen()
    print(pyfiglet.figlet_format(
        "Sunshine", font="standard", justify="center"
        ))
    print(pyfiglet.figlet_format(
        "A simple terminal based weather app",
        font="contessa", justify="center"
        ))
    print("1. Get live weather data")
    print("2. Get historical weather data")
    print("3. Exit program")
    print("Select an option by entering a number between 1-3\n")

    while True:
        choice = input("Enter your choice here: \n").strip()
        if choice == "1":
            live_weather_loop()
        elif choice == "2":
            print(
                "Not implemented yet! "
                "You will be redirected back to the main menu!"
                )
            time.sleep(5)
            main()
        elif choice == "3":
            sys.exit("GoodBye - Have a sunny day!")
        else:
            print("Invalid input, enter a number between 1 and 3")
            continue


if __name__ == '__main__':
    main()
