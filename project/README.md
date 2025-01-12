# Inventory Management System
#### Video Demo: https://www.youtube.com/watch?v=kLqbiYPsJyg
#### Description:
I have created a web application for an Inventory Management System using python, HTML, CSS and JavaScript.

I have also used the help of third party libraries and built-in frameworks
such as Python's Django ,Bootstrap for CSS, and ChartJS for Javascript

Steps to Open website:
1. Clone my project

2. I used a virtual environment called pipenv to separate the dependencies required for this project from other projects that I have. Hence you will need to

3. pip install pipenv (If not already installed)

4. Go into my base directory (cd project/finalproject)

5. Type 'pipenv shell'

6. Type 'pipenv install'(To install the dependencies)

7. Then run the application using 'python manage.py runserver'


## About how i built the Inventory Management System:

I first created an application using Django and imported external libraries to help me in this project. The application (invApp) is separated into templates, static, and its provided files.

It contains 5 main sections, the product page, the supplier page, purchase order page, sales page, and the dashboard.

I did these in a systematic manner, where I firstly created the models, then the forms, then the views, then the urls for each.

For the product page, when a form is posted, it will be shown onto the products list. This product page is connected to multiple other sections including the supplier, purchase order, and sales page.

For the supplier page, it simply lists the supplier that supplies the products in our product list, supplier and products work hand in hand, where if the supplier does not exist, the product cannot be created.

For the purchase order page, it is where we order inventory when it is low. A feature of this is that once the status of the purchase order has been set to 'received', it will update the quantity of the product ordered in the product page.

For the sales page, it consolidates and displays the total sales, total cost, products sold, and stock in hand. It shows which customers have ordered what, and it is displayed according to its status and delivery, where the orders that have been delivered will be put at the very end.

In all of these sections, i have also provided a filter, so that you can query the database. All listings can also be deleted and I have also added pagination so that the page will not look clustered.

Lastly, the dashboard, I have used chartjs to generate some data that pertains to inventory management, it is not connected to the database, and the data provided are purely arbitrary. But the displays above the charts are connected to the database, showcasing the sales statuses, best selling products as well as the amount of quantity we have left.
