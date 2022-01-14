Readme for the cerealwebapp written in the flask framework. 

To start make sure that the database is running before starting the application. There is an attached docker directory containing the startup for an empty database with the required schema
To start the webserver, make sure you activate the virtual envoirment first and use the command: flask run 

Currently the docker DB does not import any data on startup, run <webadress for server>/import when the server is running to import the test data which will import the csv data into the DB.

