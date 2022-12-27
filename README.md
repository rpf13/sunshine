# Sunshine - A CLI Weather App
The main purpose of this CLI terminal based site is, to provide weather information for any given location. It uses a simple CLI based questionary to navigate the user through the app.
It should be a fun way to get real time weather information, using the Free Weather API of [Open-Meteo](https://open-meteo.com/en)

    ADD SCREENSHOT WITH MAIN MENUE PICTURE

---


## Objectives
This sections covers the main goals, which I had in mind when creating this project. This project is purely based in Python as a simple CLI Terminal app as part of the Code Institute's Project Portfolio 3.

### Main Objectives
My goal was to learn from mistakes I did in the last two projects, specially in the planning phase.
I wanted to include an API and came along the Free Weather API of [Open-Meteo](https://open-meteo.com/en), which I really liked and in combination with using the [Geopy Library](https://pypi.org/project/geopy/), a great Python project. I wanted to cover the following main objectives:

- create user input main menu to choose for feature as well as easy CLI navigation inside each menu
- main feature to get live weather for a location anywhere in the world
- using the geopy library to find the user input location and get the latitude and longtitude information
- create a dedicated class to include the API call to the Open-Meteo API
- display the weather info received from the api (if none display error) and enrich it with further infos based on the weather code, which is part of the API result.
- Temperature and analasys of the weather code, based on [WMO Weather interpretation codes](https://open-meteo.com/en/docs#latitude=47.28&longitude=8.47&hourly=temperature_2m)
- if there is wind, it should be displayed
- option to display the weather info for a random place
- option to get historical weather data using the [Historical Open Meteo API](https://open-meteo.com/en/docs/historical-weather-api)
- show historical data for requested location getting the weather code for the daily weather summary
- display ascii art for all the various weather code interpretations

### Stretch Objectives

The following stretch objectivse are meant as a "nice to have" feature and depending on the time, I will implement them or not.

- get offline data for a specific set of cities (could be all capitals in Europe or similar) for the last year (2022)
- offline data should provide an alternate solution, if either geopy or the weather API is down
- user should have the choice, for the given city, to get the historical daily weather data, via weather code

### Logical Flowchart
The following flowchart displays the logic behind the app.

![Flowchart](docs/flowchart/sunshine_flowchart.drawio.png)

## UX & Design
This site is a pure terminal based CLI app, which has limited browser support and runs in a default terminal window size of 80 columns by 24 rows.

### User Stories

- As a visiting user, I would like to immediately understand the navigation through the app
- As a visiting user, I would like to get the live weather data for my given location
- As a visiting user, I would like ot get the live weather data for a randomly choosen location
- As a visiting user, I would like to get the historical weatehr data for a particular day in past for a particular location.
- As a visiting user, I would like to get the results of the weather displayed in a short and easy to understand format.


Welcome rpf13,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **August 17, 2021**

## Reminders

* Your code must be placed in the `run.py` file
* Your dependencies must be placed in the `requirements.txt` file
* Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

-----
Happy coding!