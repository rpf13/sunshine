# Sunshine - A CLI Weather App
The main purpose of this CLI terminal based site is, to provide weather information for any given location. It uses a simple CLI based questionary to navigate the user through the app.
It should be a fun way to get real time weather information, using the Free Weather API of [Open-Meteo](https://open-meteo.com/en)

![Techsini Screenshot](docs/testing/techsini.png)

---

## Objectives
This sections covers the main goals, which I had in mind, when creating this project. This project is purely in Python as a simple CLI Terminal app, part of the Code Institute's Project Portfolio 3.

### Main Objectives
My goal was to learn from mistakes I did in the last two projects, specially in the planning phase.
I wanted to include an API and came along the Free Weather API of [Open-Meteo](https://open-meteo.com/en), which I really liked and in combination with using the [Geopy Package](https://pypi.org/project/geopy/), I had an interesting and challenging Python project. I wanted to cover the following main objectives:

- create user input main menu to choose for a feature as well as easy CLI navigation inside each menu
- main feature to get live weather for a location anywhere in the world
- using the geopy Open StreetMap Nominatim API, to find the user input location and get the latitude and longitude information
- create a dedicated class to include the API call to the Open-Meteo API
- display the weather info received from the API and enrich it with further infos based on the weather code, which is part of the API result.
- Temperature and analysis of the weather code, based on [WMO Weather interpretation codes](https://open-meteo.com/en/docs)
- if there is wind, it should be displayed
- option to get historical weather data using the [Historical Open Meteo API](https://open-meteo.com/en/docs/historical-weather-api)
- show historical data for requested location getting the weather code for the daily weather summary, wind information
- correlate the WMO weather interpretation with emojis to display for the user

### Stretch Objectives

The following stretch objectivse are meant as a "nice to have" feature and depending on the time, I will implement them or not.

- get offline data for a specific set of cities (could be all capitals in Europe or similar) for the last year (2022)
- offline data should provide an alternate solution, if either geopy or the weather API is down
- implement a random city feature, intended for users who are curious about weather conditions anywhere in the world, without specifying a place.

## UX & Design
This site is a pure terminal based CLI app, which has limited browser support and runs in a default terminal window size of 80 columns by 24 rows.

### User Stories

- As a visiting user, I would like to immediately understand the navigation through the app
- As a visiting user, I would like to get the live weather data for my given location
- As a visiting user, I would like to get the historical weatehr data for a particular day in past for a particular location.
- As a visiting user, I would like to get the results of the weather displayed in a short and easy to understand format.
- As a visiting user, I would like to get enhanced weather information such as wind, weather condition.

---

## Features

This chapter will describe each feature of the application.

The main goal of this app was to show and improve my Python skills. The deployment via Heroku as well as the deployment template / terminal emulation inside the browser, were provided to be used in this project. With this, there came some limitations. Furthermore, this project is not responsive and runs only on bigger screens (tablet or bigger). **Please Note, this app will only run in Chrome browser, without any issues!** This is due to limitations in the way the app is deployed, made accessible as a Terminal app inside the browser as well as some browser issues. More details on that in the testing / bugs section.

### Existing Features

- Main Menu - Entry point
    - The main menu displays a nice welcome message and explains the main purpose of the app
    - It gives a clear and easy overview of the features, from which the user can choose from
    - It tells the user to make it's choice and enter the related number
    - It gives the user the possibility to start / restart the app / terminal, via the big red "Run Program" Button

    ![Main Menu](docs/testing/00_main_menu.png)

- Live weather data (Menu Item 1)
    - The first feature out of the main menu is live weather data.
    - The user get's prompted to enter a town, for which he wants live weather data.
    
        ![Live Weather Town](docs/testing/01_live_town.png)

    - Once the user has entered the town and pressed enter, he will be presented with a "best match" proposal of the town.
    - The user has the choice to accept the proposal or to deny it, because it was not the town he was looking for.
    - If he accepts the proposal and enters yes, the weather data will be shown, please scroll down a few screenshots for an explanation of this option.
    
        ![Live Weather Town Proposal](docs/testing/01_live_town_proposal.png)

    - If the user denies the proposal, he will get the option to specify the country, in which his desired town is in.

        ![Live Weather Country](docs/testing/01_live_country.png)

    - Once the user has entered the country and pressed enter, he will be presented with a "best match" proposal of the desired town, based on the country
    - The user has the choice accept or deny the proposal.
    - If he accepts the proposal and enters yes, the weather data will be shown, please scroll down a few screenshots for an explanation of this option.

        ![Live Weather Country Proposal](docs/testing/01_live_country_proposal.png)

    - If the user denies the proposal, he will get the option to specify the postal / zip code, in which his desired town is in.

        ![Live Weather ZIP](docs/testing/01_live_zip.png)

    - Once the user has entered the postal / zip code, he will be presented the final result.
    - This is the last step in the decision tree, because while have entered country, town, zip code - it is considered as a unique selection criteria.
    - The user get's displayed the info about the location he has asked for, it is the data, which the geopy Open StreetMap Nominatim database has stored for a particular location. It displays enhanced geoinfo about the location.
    - The live weather is presented, as fetched via the [Open-Meteo](https://open-meteo.com/en) database
    - The first result is the temperature.
    - The second result is the actual weathercondition, which is the translated, standardized [WMO Weather interpretation codes](https://open-meteo.com/en/docs).
    - The weathercondition gets enriched via a matching emoji, to make the interpretation more appealing.
    - The user gets asked if he wants to make another turn of live wheather, which would clear the screen and bring him back to enter a new town.

        ![Live Weather Final Result](docs/testing/01_live_final_result.png)

    - If in any of the above displayed proposals (town, country) the user enters "Y" to accept the proposal, he will  immediately get displayed the weather results, as shown in the next snapshot. The same logic / explanation is valid as previously explained.

        ![Live Weather Accept Proposal](docs/testing/01_live_accept_proposal.png)

    - If the user decides to not check another location for live weather and answer the question with "N", he will be sent back to the main menu.
    - In all the confirmation questions, if the user enters a invalid input, not entering y / n, the error is caught and he will be repeteadely asked.

        ![Error Handling Confirmation Questions](docs/testing/99_confirmation_error_handling.png)

    - The address input is validated for correct and valid input. The same applies for the country and postal code / zip input. 
    - For postalcode / zip and country input, the [postal code format](https://kb.bullseyelocations.com/article/93-postal-code-formats) and [list countries](https://www.worldometers.info/geography/alphabetical-list-of-countries/) have been considered.
    - Wrong inputs will relate to a message prompted and the user gets asked again.

        ![Input Verification & Error Handling](docs/testing/99_input_error_handling.png)

- Historical Weather Data (Menu Item 2)
    - The second feature of the main moneu is the historical weather data.
    - The user is prompted to enter a historical data, for which he wants to see the weather. The weather database is limited in historical data, therefore the user is able to ask back 50 years.
    - The input format is specified

    ![Historical Weather Date Input](docs/testing/02_hist_date.png)

    - The subsequent questions / features are the same as for the live weather with the only exception, that the wording of the answers is in "the past".
    - The decision tree itself is the same

    ![Historical Weather Final Result](docs/testing/02_hist_final_result.png)

    - If the user enters an invalid date format or a date, which is more than 50 years in past, he will get an error and will be repeatedly asked to enter a valid date.

    ![Historical Weather Date Error](docs/testing/99_date_error_handling.png)

- Weather for Random Location (Menu Item 3)
    - This feature is not implemented yet, however, since planned I left it on the main menu
    - If a user enters the option 3 for the weather of a random location, he will get a text displayed, saying that the feature is not implemented yet.
    - The user will be informed, that he well be automatically redirected to the main menu

    ![Radonm Weather](docs/testing/03_random_weather.png)

- Exit Program (Menu Item 4)
    - This feature will gracefully end the program.
    - The user gets a goodbye message displayed

    ![Exit Program](docs/testing/04_exit_program.png)

- Start / Restart Program
    - If the user has gracefully exit'ed the program or his browser did run in timeout, he can start the program via the "RUN PROGRAM" button above the terminal.

    ![Run Program Button](docs/testing/00_run_program.png)

     
### Future Features

- The Weather for Random Location (Menu Item 4) will be implemented
    - To implement this, the [Geonamescache Package](https://pypi.org/project/geonamescache/) will be used
    - The geonamescache provides various functions, the `get_cities()` function will be used and further processed, to get a random city name.
- Offline City geo-database for all capitals in the world.
    - This feature would be implemented in the way that, for whatever reason the Geopy Open StreetMap Nominatim database would not be available or a user has stressed their API and "violated" the [Usage Policy](https://operations.osmfoundation.org/policies/nominatim/)
    - This feature would store the geoinfo for all the capitals in a database, or a google spreadsheet and will then be used for the API call of the weather database.

---

## Tools & Technologies Used


---

## Data Model

### Logical Flowchart
The following flowchart displays the logic behind the app, it should be seen as kind of "wireframe", which I have used to have a rough estimate and structure, while building the code for it.

![Flowchart](docs/flowchart/sunshine_flowchart.drawio.png)

---

## Development

### Challenges & Important Notes

I did take great attention and big efforts on the error handling. Since I am using two API's, this was quite a challenge.


### Commit messages

I have decided to mostly use multiline commit messages. Commit messages are an essential part of the whole project and a single line commit message is just not enough to explain. After reading [this interesting article](https://cbea.ms/git-commit/), it was clear to me, that I have to use it.

I have decided to use (mostly) multiline commits, but using tags as described this [cheatsheet](https://cheatography.com/albelop/cheat-sheets/conventional-commits/) or as also described in the LMS of the Code Institute. I did use the following syntax guidline:
- **feat:** for feature which may or may not include a CSS part
- **fix:** for a bugfix
- **style:** for changes to CSS or to give style to the code itself
- **docs:** for changes related to documentation
- **refactor:** for refactored code, re-written code
- **maint:** for general maintenance



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