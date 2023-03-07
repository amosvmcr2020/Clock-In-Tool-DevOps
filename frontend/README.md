# The frontend

The frontend is written using the Svelte framework, a javascript framework that assists the developer in building user interfaces. The frontned calls out to the API using the `axios` package, which allows the developer to easily make a range of api calls with a low, readable amount of syntax.

The frontend provides an easy to digest user interface, from which the user can trigger and visualise the majority of the available API endpoints. The user also has access to a "database" page which allows the user to clearly view the database structure, as well as an overview of the data within each table. Additionally, from the "user" page, the user can view all stored data relevant to that user, in the same format.

## Running the frontend independently

_All of the following should be done from the frontend directory_

`cd frontend`

- Installing required javascript packages:
  `npm install`
- Running the UI:
  `npm start`
