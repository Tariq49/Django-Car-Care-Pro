# Mission Statement

"To facilitate seamless vehicle servicing experiences, our Django-powered platform connects customers and mechanics, ensuring efficient service management and transparency throughout the repair process."

# Mission Objectives

- Develop a technician approval process based on skill assessments and mechanic requests.
- Develop a user-friendly interface for customers to easily register, log in, and request vehicle servicing.
- Develop a technician approval process based on skill assessments and mechanic requests.
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
