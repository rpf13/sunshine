# This file contains all classes used in this project

import requests
import sys


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
