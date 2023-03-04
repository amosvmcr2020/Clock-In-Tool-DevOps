# Clock-In-Tool

## About the application

This application has been developed to record the 'clock-in' and 'clock-out' times of the users and to identify who is online at any given time in a list of teams.

The application consists of 4 database tables which are as follows:

- Users
- Teams
- Timesheets
- Entries

An interactive diagram of the tables can be found in the frontend of the application when logged in as any user.

## Running the app using Docker

The application has been dockerised so that it is easy for the user to run and so that it is easy to host on a cloud platform, should this be considered.

In each of the backend and frontend directories is a `Dockerfile` which defines how docker should build each aspect of the app. In the root directory there is a `docker-compose.yaml` file which defines how to build and run the entire application using only one command:

- `docker-compose up --build`

Within the `docker-compose.yaml` there is also a database service which starts a postgres image and sets the appropriate environment variables for the backend to link up to it.

## About the CI/CD Pipeline

This application is source controlled using git and pushed to a repository on github. Within github there is a feature called "github actions" which enables the user to define a collection of steps to run whenever new code is pushed or merged in the repository.

These actions can be found in the `.github/workflows/app.yaml` file, where a series of jobs have been defined. These jobs include the following:

- Prettier
  - Runs prettier code formatting on all the frontend js files.
- Black
  - Runs black code formatting on all the backend python files.
- Python Autoflake
  - Removes all unused variables on the backend .
- NPMAudit
  - Runs npm audit on the frontend to scan for any vulnerabilities and notify the user.
- Pytest
  - Runs all of the tests on the backend and fails the run if any tests fail.
- PipUpgrade
  - Runs pip-upgrade on the backend to ensure no outdated dependencies are being used, otherwise the build fails.
- DockerUI
  - Build the frontend docker image and pushes it to the github image repository.
- DockerAPI
  - Build the backend docker image and pushes it to the github image repository.

From the repository, all CI/CD pipeline runs can be found under the 'actions' tab in github.

## About the backend

The backend has been written using FastAPI, a Python framework for creating restful applications. FastAPI was chosen due to its vast documentation alogside the automatically generated docs for the API itself. Once running, these are available at the "/docs" or the "/redoc" endpoint of the api. For example:
`http://0.0.0.0:8000/docs`

To link the Python API to the postgres database, SQLAlchemy was used. This enables simple connections and removes any need for proper SQL knowledge, only Python. The setup of the database using SQLAlchemy can be seen in the following files:

- `database.py`
- `models.py`

Meanwhile the actual CRUD actions can be seen in the following files:

- `main.py`
- `create_db.py`
- `create_test_db.py`

All of the API endpoints can be found in the `main.py` file, which define how the user can interact with the database. Additionally, lots of validation is involved in this file so that there is minimal risk of any user fault.

The backend is tested using the pytest framework. Pytest can be used to write a series of unit tests to ensure that the application is running as expected. Within the `test_main.py` file are tests that attempt to call the API with proper responses, as well as improper to ensure the error handling is working correctly.

Within the test file, the `create_test_db.py` script is run. This script, similarly to the `create_db.py` script, drops all existing tables and creates the four new ones populated by 2 teams, colectively containing 3 users. Each user has a timesheet allocated to them and the Administrator has 3 entries added to their timesheet.

Currently, this is run in the `main.py` folder as well in order to generate some test data whenever the application is run. Naturally, this would not be the case should this application be used in production as it would overwrite all previous data.

## Running the backend independently

### All of the following should be done from the backend:

`cd backend`

- Creating and running the python environment:
  `python3 -m venv env` &
  `source env/bin/activate`

- Pip install the required packages:
  `pip install -r requirements.txt`

- Create db:
  `python3 create_db.py`
- Running the API:
  `uvicorn app.main:app --reload`
- Test the app:
  `pytest`

## About the frontend

The frontend is written using the Svelte framework, a javascript framework that assists the developer in building user interfaces. The API is linked to the frontend using the axios package, which allows the developer to easily make a range of api calls with a low, readable amount of syntax.

The frontend provides an easy to digest user interface, from which the user can trigger and visualise the majority of the available API endpoints. The user also has access to a "database" page which allows the user to clearly view the database structure, as well as an overview of the data within each table. Additionally, from the "user" page, the user can view all stored data relevant to that user, in the same format.

## Running the frontend independently

### All of the following should be done from the frontend:

`cd frontend`

- Installing required javascript packages:
  `npm install`
- Running the UI:
  `npm start`
