# CS50 Web Development Final Project - StockSimulator

For my final project I have created a web application which serves as a visualisation tool to allow users to see how their market insights might affect a stock. It allows a user to define their own custom stocks and simulate their performance if the stock were in a bubble. It does this by allowing the user to define a volatility as well as average annual change for the stock. The user can then also define events which happen throughout the year and they can define the impact these events will have on the stocks. They can then run the simulation which will attempt to model how the stock changes throughout the year.

# How to use
The default route leads to the home page with a navigation bar at the top. From here you can click register and make an account. Once you have an account, navigate to the **Stocks** tab where you can create your own stocks. You can then navigate to the **Portfolio** tab and add a desired amount of the stock to your portfolio before navigating to the **Events** tab and defining some events. Both stocks and events can be edited by being clicked on in their respective tabs. Once you are happy, you can navigate to the **Simulator** tab. From here you can add your events to the simulator and specify a date on which they occur. You can then press the **Start Simulation** button which will run the simulation and then jump to the simulation results.


# Distinctiveness and Complexity

My StockSimulator web application is distinct from other projects in this course and shares little similarity with them. It is to be used a tool for individuals rather than a service like the other projects in the course, such as the auction or social network. While the other projects focus on a platform which facilitates some level of communication between multiple users, my application performs a task for the user rather than connect two users. 

It is also sufficiently complex as it involves multiple javascript files as well as more complicated bootstrap concepts than those shown in the course, allowing for greater customisation and mobile responsiveness. It also makes use of additional javascript frameworks such as eCharts and uses multiple models on the backend with different relationships including a many to many relationship.

# Project Layout and Code

## File Layout

The project is split up with JavaScript and CSS files found under `app/static/app` and HTML templates found under `app/templates/app`. The app directory also contains all the python files generated by a django project as well as an additional `forms.py` file which contains django forms.

## JavaScript Files

There are two JavaScript files. The first is `charts.js` and it contains functions for creating a line chart as well as a doughnut chart using eCharts. These functions are then used elsewhere such as in the second file which is `simulator.js`. This file is responsible for adding and removing events in the simulator page as well as generating and displaying all of the simulation results when the start simulation button is pressed. 

## HTML Templates

There are a total of 10 HTML template files with 9 of them corresponding to a page in the application. They all inherit from a `layout.html` file which defines the basic layout of the page including the navigation bar at the top of the page. These templates all use django's formatting language to customise the page and make it dynamic.

## Python Files

The `forms.py` file contains forms which are used to receive data from the front end. These include forms for creating and editing stocks and well as creating and editing events. The `models.py` file then defines four models. There is a *Stock* model, an *Event* model and a *Portfolio* model as well as a *StockInPortfolio* model which is used as a linking table between the *Stock* and *Portfolio* models. The `urls.py` file then defines the urlpatterns for the application and the `views.py` file defines each view.

### `views.py`
The `views.py` file contains the following functions:
- `index` - This defines the default view for the application.
- `login_view`, `logout_view`, `register` - These are basic views for user authentication.
- `stocks`, `new_stock`, `edit_stock`, `delete_stock` - These views allow you to view or create stocks depending on whether they receive a get or post request.
- `events`, `new_event`, `edit_event`, `delete_event` - These views allow you to view or create events depending on whether they receive a get or post request.
- `portfolio`, `add_stock`, `remove_stock` - These views allow you to view your portfolio as well as add and remove stocks to/from it.
- `simulator`, `simulation` - These views run the simulation itself and the latter returns a JsonResponse containing the results.


# How to run the application

To run the application you must first run the following commands to get the latest migrations:
- `python manage.py makemigrations app`
- `python manage.py migrate`

Once you have made the migrations you can run `python manage.py runserver` to start the application.

# Third-Party Packages

I have used a few different frameworks to help create the front end. Alongside bootstrap's CSS, I have included it's JavaScript bundle which includes `popper.js` which I use for customising tooltip content. I have also used [Apache Echarts](https://cdn.jsdelivr.net/npm/echarts@5.5.1/dist/echarts.min.js) to create line and doughnut charts. In the backend, I have used numpy as part of the simulation.