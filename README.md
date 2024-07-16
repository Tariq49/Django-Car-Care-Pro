# Mission Statement

"To facilitate seamless vehicle servicing experiences, our Django-powered platform connects customers and mechanics, ensuring efficient service management and transparency throughout the repair process."

# Mission Objectives

- Develop a technician approval process based on skill assessments and mechanic requests.
- Develop a user-friendly interface for customers to easily register, log in, and request vehicle servicing.
- Establish a feedback system for customers to provide reviews and suggestions regarding service quality.
- Enable customers to view and manage invoices and track the progress of their vehicle repairs.


# Instructions to run pogram

- Open a terminal
- Run following commands

Create DataBase

```psql
psql -U postgres
CREATE DATABASE car_care_pro_django;
\q
```

### Please note that the commands for setting up the development environment, creating migrations, and applying them to the database are written in the Makefile for convenience.

The command is used to install the Python packages listed in a specific requirements file.

```psql
make dev-install
```

The command starts the Django development server using the settings defined in the config/settings/dev.py file. After starting the server, Django typically outputs a message indicating the URL where you can access your application.

```psql
make start
```

Once the server starts, you should see output similar to:

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
July 08, 2024 - 12:34:56
Django version X.Y.Z, using settings 'config.settings.dev'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

#### Accessing your Application
- Open your web browser and navigate to http://127.0.0.1:8000/ or http://localhost:8000/.

- You should now see your Django application running locally. Any changes you make to your code will be reflected upon refreshing the page.

#### Additional Notes
- To stop the development server, press CONTROL-C in the terminal where it is running.

#### Django Development Commands
The command is used to create a new superuser for your Django project with a specified settings module.

```
make dev-super
```

When you create a new database for your Django project, running this command is an essential step to set up the database schema according to your models and their migrations.

```
make dev-m
```

This command will scan the models.py file for changes, create a new migration file in the migrations directory of the app, and ensure that it uses the settings specified in config/settings/dev.py.

```
make dev-makem
```

Django uses migrations to track changes to your models over time. Running migrate applies these changes to your database schema, ensuring it stays synchronized with your model definitions.

```
make dev-m
```

The command is used to display a list of all the migrations in your Django project and their current status, using a specific settings module.

```
make dev-showm
```

The command is used to open a database shell for your Django project's database, using a specific settings module.
```
make dev-dbshell
```

The command is used to open an interactive Python shell with your Django project's context, using a specific settings module.

```
make dev-shell
```

The command is used to display the SQL statements for a specific migration in your Django project

```
make dev-sqlm
```
