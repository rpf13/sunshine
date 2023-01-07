# This file contains all classes used in this project

import requests
import sys
import re
import datetime


# Main class to execute the API calls and do the error handling.
class MeteoDataCall:
    """
    Class to execute api call for live and historical
    weather on open-meteo.com. Error handling done at
    this stage.
    """
    def __init__(self, coordinates):
        # instance attributes
        self.coordinates = coordinates

    def live_data(self):
        """
        Method to call API for live data and return json
        If call is unsuccessful, start exception handling.
        """
        url = f"https://api.open-meteo.com/v1/forecast?latitude={self.coordinates[0]}&longitude={self.coordinates[1]}&current_weather=true&windspeed_unit=kmh"  # noqa
        # Create the actual api call. If the request is successful,
        # the raise_for_status() method is called to check for any HTTP errors,
        # such as a 4xx or 5xx status code.
        # If no errors are found, the JSON response is returned.
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        # Handle known HTTP error and exit
        except requests.exceptions.HTTPError as error:
            sys.exit(
                "An error has occured when calling the Open-Weather API \n"
                "Unfortunately we cannot get the weather data now. \n"
                "Please try again later! \n"
                "The API has returned the status code: {}".format(error)
                )
        # Handle any unknown API error and exit
        except Exception as error:
            sys.exit(
                f"There was an undefined error with the Open-Weather API \n"
                "Please try again later"
                )

    def historical_data(self, hist_date):
        """
        Method to call API for historical data and return json
        If call is unsuccessful, start exception handling.
        """
        self.hist_date = hist_date
        url = f"https://archive-api.open-meteo.com/v1/era5?latitude={self.coordinates[0]}&longitude={self.coordinates[1]}&start_date={self.hist_date}&end_date={self.hist_date}&daily=weathercode,temperature_2m_max,windspeed_10m_max&timezone=auto"  # noqa
        # Create the actual api call. If the request is successful,
        # the raise_for_status() method is called to check for any HTTP errors,
        # such as a 4xx or 5xx status code.
        # If no errors are found, the JSON response is returned.
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        # Handle known HTTP error and exit
        except requests.exceptions.HTTPError as error:
            sys.exit(
                "An error has occured when calling the Open-Weather API \n"
                "Unfortunately we cannot get the weather data now. \n"
                "Please try again later! \n"
                "The API has returned the status code: {}".format(error)
                )
        # Handle any unknown API error and exit
        except Exception as error:
            sys.exit(
                f"There was an undefined error with the Open-Weather API \n"
                "Please try again later"
                )


# Class to verify if the date input for the historical option
# is valid or not.
class DateInputVerifier:
    """
    Date verification class, used to verify user input. It checks
    if input is valid in terms of month, day numbers and it
    checks if year is max. 50 years back, since open-weather API
    does not support endless historical data
    """
    def __init__(self):
        self.pattern = r"^\d{4}-\d{2}-\d{2}$"

    def is_valid(self, date):
        """
        Verify that the input string matches the
        desired time format (YYYY-MM-DD) and is valid
        Returns boolean value used further in the calling part
        """
        # Check if the date matches the pattern
        if not re.match(self.pattern, date):
            return False

        # Split the date into year, month, and day
        year, month, day = date.split("-")
        year, month, day = int(year), int(month), int(day)

        # Check if the month is within the range of 1-12
        if month < 1 or month > 12:
            return False

        # Check if the day is within the range of 1-31
        if day < 1 or day > 31:
            return False

        # Check if the year is within the range of 50 years back in time
        current_year = datetime.datetime.now().year
        if year > current_year or year < current_year - 50:
            return False

        # If all checks pass, return True
        return True
