# The Backend 
## Running the backend independently

*All of the following should be done from the backend directory*

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