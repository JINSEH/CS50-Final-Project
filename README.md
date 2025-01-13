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

5. Type 'pipenv shell' in the terminal

6. Type 'pipenv install'(To install the dependencies) in the terminal

7. Then run the application using 'python manage.py runserver' in the terminal


## About how i built the Inventory Management System:

I first created an application using Django and imported external libraries to help me in this project. The application (invApp) is separated into templates, static, and its provided files.

It contains 5 main sections
> 1. The product page 
>2. The supplier page
>3. The purchase order page
>4. The sales page
>5. The dashboard.

I did these in a systematic manner, where I firstly created the models, then the forms, then the views, then the urls for each.


## What each page contains
For the product page, when a form is posted, it will be shown onto the products list. This product page is connected to multiple other sections including the supplier, purchase order, and sales page.

For the supplier page, it simply lists the supplier that supplies the products in our product list, supplier and products work hand in hand, where if the supplier does not exist, the product cannot be created.

For the purchase order page, it is where we order inventory when it is low. A feature of this is that once the status of the purchase order has been set to 'received', it will update the quantity of the product ordered in the product page.

For the sales page, it consolidates and displays the total sales, total cost, products sold, and stock in hand. It shows which customers have ordered what, and it is displayed according to its status and delivery, where the orders that have been delivered will be put at the very end.

In all of these sections, i have also provided a filter, so that you can query the database. All listings can also be deleted and I have also added pagination so that the page will not look clustered.

Lastly, the dashboard, I have used chartjs to generate some data that pertains to inventory management, it is not connected to the database, and the data provided are purely arbitrary. But the displays above the charts are connected to the database, showcasing the sales statuses, best selling products as well as the amount of quantity we have left.

## What each file contains:
Folders:
1. finalproject:
> This folder is the base directory for the web application. It contains very important files including:
>> 1.  settings.py
>>> This file stores configuration information in Django
>> 2. urls.py
>>> This file is used to route users to the appropriate content or functionality when they visit my web application.

Before moving on to the main files that I have created, there are other files that needs explanation: 

> sqlite3.db
 Django uses sqlite3 as its default database engine. I used it because it was sufficient for my project.

>Pipfile and pipfile.lock
>> Contains dependencies necessary for this project, it was made using pipenv, which is a tool that provides all necessary means to create a virtual environment. 
>>> Why use a virtual environment?
>>>> By using a virtual environment, we are able to run the programs with the same dependencies, without it clashing with dependencies of other projects.

2. invApp
> 1. migrations:
>> When changing your models, migrations are Django's way of propagating changes (Adding a field, deleting a model, etc.) you make to your models into your database schema.
> 2. Static
>> Contains a few files:
>>> 1. styles/styles.css: 
>>>> Contains custom styling for the HTML<hr>
>>> 2. images: 
>>>> Contains every single image used in my project<hr>
>>> 3. js/index.js: 
>>>> Contains the javascript/ChartJS code for the charts in dashboard page. 
> 3. templates
>> Contains every single template (Design for pages)
> 4. filters.py
>> This file contains the search query/filters you see in the different sections. 
> 5. forms.py
>> This file contains what each form of the different sections should include (Such as its input fields), and set limitations that can check the inputs before being given to the backend. 
> 6. models.py
>> This file is directly correlated with the database, all of my database schema are created here.
> 7. views.py
>> This defines the logic of the website, it is essentially the backend. Here you define which template will be shown, where the user will go after inputting the data, and what happens to the data itself.  
> 8. urls.py
>> This file maps the urls to views, meaning after a view has been created, what is the url to get to that view. 