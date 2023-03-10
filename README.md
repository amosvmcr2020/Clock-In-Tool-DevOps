# Clock-In-Tool

## About the application

This application has been developed to record the 'clock-in' and 'clock-out' times of the users and to identify who is online at any given time in a list of teams.

The application consists of 4 database tables which are as follows:

- Users
- Teams
- Timesheets
- Entries

An interactive diagram of the tables can be found in the frontend of the application when logged in as any user.

## Application Technology Stack

This application is build using the following technologies:

- Backend
  - Python FastAPI which can be served using a `uvicorn` server.
  - Postgres SQL relational database.
- Frontend
  - SvelteJS frontend framework

## Running the app using Docker

In each of the backend and frontend directories is a `Dockerfile` which defines how docker should build each aspect of the app. In the root directory there is a `docker-compose.yaml` file which defines how to build and run the entire application using only one command:

- `docker-compose up --build`

Within the `docker-compose.yaml` there is also a database service which starts a postgres image and sets the appropriate environment variables for the backend to link up to it.

There is more information on how to run each aspect of the app individually in the `frontend` and `backend` readme files.

## The Backend

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
