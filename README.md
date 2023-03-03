# Clock-In-Tool

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

## Running the backend

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

## Running the frontend

### All of the following should be done from the frontend:

`cd frontend`

- Installing required javascript packages:
  `npm install`
- Running the UI:
  `npm start`
