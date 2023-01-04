# This file contains all classes used in this project

import requests
import sys
import re


class MeteoDataCall:
    """
    Class to execute api call for weather on open-meteo.com
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
                "Error details: {}".format(error)
                )
        # Handle any unknown API error and exit
        except Exception as error:
            sys.exit(
                f"There was an undefined error with the Open-Weather API \n"
                "Please try again later"
                f"Error details: {error}"
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
                "Error details: {}".format(error)
                )
        # Handle any unknown API error and exit
        except Exception as error:
            sys.exit(
                f"There was an undefined error with the Open-Weather API \n"
                "Please try again later"
                f"Error details: {error}"
                )


class TimeInputVerifier:
    def __init__(self):
        self.pattern = r"^\d{4}-\d{2}-\d{2}$"

    def verify(self, input_string: str) -> bool:
        """
        Verify that the input string matches the
        desired time format (YYYY-MM-DD).
        """
        return bool(re.match(self.pattern, input_string))
