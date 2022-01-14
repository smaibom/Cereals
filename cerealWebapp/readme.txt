To setup the virtual envoirment in windows:
Be in the cerealswebapp folder in your terminal 

<python3.10> -m venv venv

run the activate file created in the venv/scripts/ folder to start the virtual envoirment

when in the virtual envoirment run packages.ps1 to install the required packages for python

set the envoirment value $env:FLASK_APP="__init__.py" if using powershell to give entry point for flask

now start webserver by running

flask run

flask server runs default on http://127.0.0.1:5000/