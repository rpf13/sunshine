# Testing

Return back to the [README.md](README.md) file.

I have invested quite some efforts to do proper testing of the (deployed) application. I did try to catch all sorts of errors of the API's as well errors for wrong user input. This is also explained in the Development section of the README file.
I did try to simulate some of the API errors, as it can be seen in the coming chapters. However, I could not simulate each and every possible error, therefore I did add a lot of generic error handling in the try / except blocks.

## Python Code Validation

I have used the recommended [CI Python Linter](https://pep8ci.herokuapp.com) to validate all of my Python files.

The CI Python Linter can be used two different ways.
- Copy/Paste your Python code directly into the linter.
- As an API, using the "raw" URL appended to the linter URL.
    - To find the "raw" URL, navigate to your file directly on the GitHub repo.
    - On that page, GitHub provides a button on the right called "Raw" that you can click on.
    - From that new page, copy the full URL, and paste it after the CI Python Linter URL (with a `/` separator).
    - Examples:

    | File | CI URL | Raw URL | Combined |
    | --- | --- | --- | --- |
    | PP3 *run.py* file | `https://pep8ci.herokuapp.com/` | `https://raw.githubusercontent.com/rpf13/sunshine/main/run.py` | `https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/rpf13/sunshine/main/run.py` |

I have used the "raw" url-method to validate my python files. I did spend quite some efforts to be inline with the requirement of not exceeding 80 characters in width, for any code line. However, in case of the API url's, I could not find a way to insert a new line, therefore I have used the `noqa` = **NO Quality Assurance** tag in the code.

Code Validation Summary Table

Below a table with the summary of the Python checker. The CI Linter URL is included, as well as a link to the related screenshot.

| File | CI URL | Screenshot | Notes |
| --- | --- | --- | --- |
| run.py | [CI PEP8](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/rpf13/sunshine/main/run.py) | [screenshot](docs/testing/pep8_main.png) | All clear, no errors found |
| classes.py | [CI PEP8](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/rpf13/sunshine/main/classes.py) | [screenshot](docs/testing/pep8_classes.png) | All clear, no errors found |
| my_emoji.py | [CI PEP8](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/rpf13/sunshine/main/my_emoji.py) | [screenshot](docs/testing/pep8_my_emoji.png) | All clear, no errors found |


## Lighthouse Testing

Even though this is a terminal based cli app, I wanted to run the lighthouse test, to see the performance. Since the deployment template and all it's settings was given by Code Institute as a requirement, I did not change anything on it. I think the testing results are fine.

![Lighthouse](docs/testing/lighthouse.png)


## User Stories Testing

This chapter will focus on the user story testing, giving a snapshot for each feature.

| User Story | Screenshot | Notes |
| --- | --- | --- |
| - As a visiting user, I would like to immediately understand the navigation through the app | [screenshot1](docs/testing/00_main_menu.png) & [screenshot2](docs/testing/01_live_country_proposal.png) | This has been achieved via the simple menu and the exact questions / possible answers for each section |
| - As a visiting user, I would like to get the live weather data for my given location | [screenshot](docs/testing/01_live_accept_proposal.png) | Any possible location can be set as the input |
| - As a visiting user, I would like to get the historical weatehr data for a particular day in past for a particular location. | [screenshot](docs/testing/02_hist_final_result.png) | The historical weather let's the user check any location for the last 50 years |
| - As a visiting user, I would like to get the results of the weather displayed in a short and easy to understand format. | [screenshot](docs/testing/01_live_final_result.png) | The weather data get's displayed in a simple way; the temperature is a clear number and the weather interpretation is achieved via a short but distinctive sentence - supported via the emoji's. The wind is also displayed an easy to understand format. |
| - As a visiting user, I would like to get enhanced weather information such as wind, weather condition. | [screenshot](docs/testing/02_hist_final_result.png) | Wind and weather condition are part of every reply |


## Browser Compatibility
The main validation of the app has been done via Chrome on Mac OS X. However, I did test it on furhter browsers and OS's.
The following table will give an overview of all combinations, where the site has been tested. Browser compatibility is very limited, but this is due to the nature of this terminal emulated app inside a browser.

|                           | Chrome |        Firefox        | Safari | Edge |                                                                     Notes                                                                     |
|:-------------------------:|:------:|:---------------------:|:------:|:----:|:---------------------------------------------------------------------------------------------------------------------------------------------:|
| OS X 13.1 MacBook Pro 16" |  PASS  | PASS (w. Limitations) |  FAIL  | N.A. | See Bugs Section for info regarding Firefox. Safari does not seem to be supported with this deployment template, it wont even correctly start |
|  iPadOS 16.2 iPad Pro 11" |  N.A.  |          N.A.         |  N.A.  | N.A. | iPad / Tablets do not seem to work, the page loads but input is not possible.                                                                 |
|    Windows 10 Pro 21H1    |  PASS  | PASS (w. Limitations) |  N.A.  | PASS |                                                                                                                                               |
|       Mobile Phones       |  N.A.  |          N.A.         |  N.A.  | N.A. | Mobile Phones not supported due to the fixed setting of the terminal in the App                                                               |


## Error Handling Testing


## Using Python's breakpoint() feature

## Bugs

### Open Bugs

### Closed Bugs







    TODO: Add comment on limitations / browser support

    TODO: Add separate chapter on how I have used breakpoint() to tshoot inline