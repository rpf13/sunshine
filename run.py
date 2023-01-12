import geopy
from geopy.geocoders import Nominatim
from classes import MeteoDataCall
from classes import DateInputVerifier
import my_emoji
import os
import pyfiglet
import time
import sys
import re


# Clear screen function, used on various places in the code
def clear_screen():
    """
    Clear screen function to clean up the terminal
    """
    os.system("cls" if os.name == "nt" else "clear")


# Generic function to validate user input
def ask_input(question, options):
    """
    This function is generic and validates the user input.
    The question to display is one argument.
    The options (possible answers) is another argument,
    an array is expected.
    If user inputs anything else than the expected answer,
    he will be prompted again, using the options as possible
    answer (join method used, / as delimiter).
    """
    answer = input(question).upper().strip()
    if answer in options:
        return answer
    else:
        print(f"Please input {'/'.join(options)} only!")
        return ask_input(question, options)


# The following functions will validate the user input required
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
    Calls validate_input function.
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
    Calls validate_input function.
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
    Validate the input string to match all possible characters,
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
    Calls validate_postalcode function.
    """
    while True:
        postalcode = input(
            "What is the zip / postal code of your town? \n"
        ).rstrip()
        if validate_zip_input(postalcode):
            return postalcode
        else:
            print(f"{postalcode} is not valid, try again!")


# Function to get geodata from geopy module (api), the Nominatim
# Open Street Map module of the geopy.
def get_location():
    """
    This function is used to get the latitude/longitude of a specific town,
    required for the open-meteo api call. User gets prompted to input a town,
    country or postal code. The input is used to get the data via the OSM
    Nominatim module, which is basically an api call. Return value is an
    array with the latitude, longitude value.
    """
    # get the address by calling function,
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

    confirm = ask_input("Can you confirm? Y/N \n", ["Y", "N"])
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
        confirm = ask_input("Can you confirm? Y/N \n", ["Y", "N"])
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
                    f"{location}."
                )
            else:
                print("This place does not seem to exist!")
                return
    # geopy will return lat/long values, which get stored in array
    coordinates = [location.latitude, location.longitude]
    return coordinates


# Translate the weathercode from weather api call
def translate_weathercode(weathercode):
    """
    Function to translate the received WMO weathercode into
    a human readable code, using the translation table on
    open-meteo.com api reference.
    Originally I wanted to create a match case but
    unfortunately the gitpo python version does not support
    it (needs 3.10)
    """
    weathercode = weathercode
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
    emoji's from the my_emoji CONDITIONS hash. Further Error
    handling is done.
    """

    # Verify if the geopy lookup did return anything, if None and hence
    # there was an error, exit program and report.
    coordinates = get_location()
    if coordinates is None:
        sys.exit(
            "There was an error when calling the Open StreetMap \n"
            "API to get the desired location data. \n"
            "Please try again later. \n"
            "Exiting Program."
        )

    # Call the Meteo API Class and the live_data method
    api_fetcher = MeteoDataCall(coordinates)
    weatherdata = api_fetcher.live_data()

    # Call the translate_weathercode function, handover code
    # and assign return value to weathercondition variable
    weathercondition = translate_weathercode(
        weatherdata["current_weather"]["weathercode"]
        )
    temperature = weatherdata["current_weather"]["temperature"]
    windspeed = weatherdata["current_weather"]["windspeed"]

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
    # If there is valid weathercode but not really wind
    elif weathercondition != "none" and windspeed <= 2:
        print(
            "The weather at this location is "
            f"{weathercondition} "
            f"{my_emoji.CONDITIONS[weathercondition.replace(' ', '_')]}\n"
            f"There is no wind"
        )


# Loop for live weather function, until user decides to leave
def live_weather_loop():
    """
    This function creates a live_weather loop, asking the user repeatedly
    if he wants to take another live_weather round. If negative, will
    bring the user back to the main menu via calling main().
    """
    while True:
        clear_screen()
        get_live_weather()
        answer = ask_input(
            "Do you want to get the weather for another location? Y/N \n",
            ["Y", "N"])
        if answer == "N":
            return


# Function to get historical weather from related resources
def get_historical_weather():
    """
    This function gets all necessary data for the historical weather,
    calls the required functions and classes and prints the
    result to the user. It will enhance the data with related
    emoji's from the my_emoji CONDITIONS hash. Further error
    handling is done. It starts with verifying the date, which
    the user imputs, via calling the dedicated class.
    """
    verify_date = DateInputVerifier()
    # Ask and Verify for historical date, repeat question if
    # input format is wrong.
    while True:
        hist_date = input(
            "For which date you would like to get the weather? \n"
            "Historical weather is available for the last 50 years \n"
            "Enter the date in the format YYYY-MM-DD \n"
            ).strip()
        if verify_date.is_valid(hist_date):
            break
        else:
            print("Invalid input, enter a valid date")
            continue

    # Verify if the geopy lookup did return anything, if None and hence
    # there was an error, exit program and report.
    coordinates = get_location()
    if coordinates is None:
        sys.exit(
            "There was an error when calling the Open StreetMap \n"
            "API to get the desired location data. \n"
            "Please try again later. \n"
            "Exiting Program."
        )

    # Call the Meteo API Class and the historical data method
    api_fetcher = MeteoDataCall(coordinates)
    weatherdata = api_fetcher.historical_data(hist_date)

    # Call the translate_weathercode function, handover code
    # and assign return value to weathercondition variable
    weathercondition = translate_weathercode(
        weatherdata["daily"]["weathercode"][0]
        )
    temperature = weatherdata["daily"]["temperature_2m_max"][0]
    windspeed = weatherdata["daily"]["windspeed_10m_max"][0]

    # Print historical temperature for desired location
    print(
        f"On the {hist_date}, "
        f"the daily max. temperature there was: {temperature} ℃"
    )
    # If there is a valid weathercode and significant windspeed
    if weathercondition != "none" and windspeed > 2:
        print(
            "The weather at this location was "
            f"{weathercondition} "
            f"{my_emoji.CONDITIONS[weathercondition.replace(' ', '_')]}\n"
            f"There was a max wind speed of {windspeed} km/h"
        )
    # If there is valid weathercode but not really wind
    elif weathercondition != "none" and windspeed <= 2:
        print(
            "The weather at this location was "
            f"{weathercondition} "
            f"{my_emoji.CONDITIONS[weathercondition.replace(' ', '_')]}\n"
            f"There was no wind"
        )


# Loop for historical weather function, until user decides to leave
def historical_weather_loop():
    """
    This function creates a historical_weather loop, asking the user repeatedly
    if he wants to take another historical_weather round. If negative, will
    bring the user back to the main menu via calling main().
    """
    while True:
        clear_screen()
        get_historical_weather()
        answer = ask_input(
            "Do you want to get the weather for another location? Y/N \n",
            ["Y", "N"])
        if answer == "N":
            return


# Main function to control the tool, display menu to user
def main():
    """
    This is the main function and the starting point of the tool.
    It will clear the screen and display the menu to the user.
    It will request the user to enter the number for one of the
    given options. Error handling of input is done.
    """

    while True:
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
        print("3. Get weather for random location")
        print("4. Exit program")
        print("Select an option by entering a number between 1-4\n")
        choice = input("Enter your choice here: \n").strip()
        if choice == "1":
            live_weather_loop()
        elif choice == "2":
            historical_weather_loop()
        elif choice == "3":
            print(
                "Not implemented yet! "
                "You will be redirected back to the main menu!"
                )
            time.sleep(5)
            main()
        elif choice == "4":
            sys.exit("GoodBye - Have a sunny day!")
        else:
            print("Invalid input, enter a number between 1 and 4")
            continue


# Boilerplate to make sure, methods are only called automatically,
# if program is directly called via main().
if __name__ == '__main__':
    main()
