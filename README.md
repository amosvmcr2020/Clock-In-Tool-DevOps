# Clock-In-Tool

## About the backend
The backend has been written using FastAPI, a Python framework for creating restful applications. FastAPI was chosen due to its vast documentation alogside the automatically generated docs for the API itself. Once running, these are available at the "/docs" or the "/redoc" endpoint of the api. For example: 
`http://localhost:8000/docs`

To link the Python API to the postgres database, SQLAlchemy was used. This enables simple connections and removes any need for proper SQL knowledge, only Python. The setup of the database using SQLAlchemy can be seen in the following files: 
- `database.py`
- `models.py`

Meanwhile the actual CRUD actions can be seen in the following files: 
- `main.py`
- `create_db.py`
- `create_test_db.py`

All of the API endpoints can be found in the `main.py` file, which define how the user can interact with the database. Additionally, lots of validation is involved in this file so that there is minimal risk of any user fault. 

## Running the backend
### All of the following should be done from the backend:
`cd backend`

* Creating and running the python environment
`python3 -m venv env`
`source env/bin/activate`

* Pip install the required packages
`pip install -r requirements.txt`


* Create db
`python3 create_db.py`
* Running the API
`uvicorn main:app --reload`
* Test the app
`pytest`

## About the frontend
The frontend is written using the Svelte framework, a javascript framework that assists the developer in building user interfaces. The API is linked to the frontend using the axios package, which allows the developer to easily make a range of api calls with a low, readable amount of syntax.

## Running the frontend
### All of the following should be done from the frontend: 
`cd frontend`

* Installing required javascript packages
`npm install`
* Running the UI
`npm start`