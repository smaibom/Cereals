from flask import Blueprint, render_template, request,flash
from flask.helpers import url_for
from flask_login import login_required
from werkzeug.utils import redirect
from . import db
import pandas as pd
from .models import Cereal
from .helperfuncs import get_value, set_cereal_value

"""
Cereal blueprint functions are placed here

Currently the table for cereals contains picture file ID so the use of iloc[:,:-1] is for removing the last column for display
TODO: Move pictures to own table, use foreign key relation to link to main table
"""

cereal = Blueprint('cereal', __name__)

@cereal.route('/list')
def list():
    #Get all cereals in database
    df = pd.read_sql("SELECT * FROM cereal", db.engine).iloc[:,:-1]
    #Get headers and data from the dataframe and display on webpage
    cerealdata =df.to_dict('index')
    cerealheaders = df.to_dict().keys()
    return render_template('cereals.html', cereals = cerealdata, headers = cerealheaders )

@cereal.route('/list/<int:id>')
def list_with_id(id):
    #Get specific ID Cereal 
    df = pd.read_sql("SELECT * FROM cereal WHERE id = %s" %id, db.engine)
    if df.empty:
        flash('Requested cereal ID dosent exists')
        return redirect(url_for('cereal.list'))
    image = df.iloc[0,-1]
    imageloc = url_for('static', filename = image)
    df = df.iloc[:,:-1]
    #Get headers and data from the dataframe and display on webpage
    cerealdata =df.to_dict()
    cerealheaders = df.to_dict().keys()
    return render_template('cereal.html', cereals = cerealdata, headers = cerealheaders, id = id, image = imageloc)

@cereal.route('/list/delete',methods = ["POST"])
@login_required
def delete_id():
    """
    Function for deleting cereal IDs when user presses delte in the specific cereal page, this is a POST request as html tags only allow GET and POST
    requires login
    """
    #We get the ID from the post request and delete it and redirect back to list view
    id = request.form.get('id')
    Cereal.query.filter(Cereal.id == id).delete()
    db.session.commit()
    flash("Cereal deleted")
    return redirect(url_for('cereal.list'))

@cereal.route('/list',methods=['POST'])
def filter():
    """
    Post function for when the user presses the filter button on the webpage, 
    displays the list of cereal based on the given filter
    """
    #Get user input
    field = request.form.get('field')
    op = request.form.get('operator')
    value = request.form.get('value')
    #Get entire cereals
    df = pd.read_sql("SELECT * FROM cereal", db.engine).iloc[:,:-1]
    try:
        #Make value into correct datatype for filtering
        value = get_value(field,value)
        if op == 'eq':
            df = df.loc[df[field] == value] 
        elif op == 'noteq':
          df = df.loc[df[field] != value]   
        elif op == 'greater':
            df = df.loc[df[field] > value] 
        elif op == 'less':
            df = df.loc[df[field] < value] 
        elif op == 'lesseq':
            df = df.loc[df[field] <= value] 
        elif op == 'greatereq':
            df = df.loc[df[field] >= value] 
        cerealdata =df.to_dict('index')
        cerealheaders = df.to_dict().keys()
        return render_template('cereals.html', cereals = cerealdata, headers = cerealheaders )
    except:
        flash('invalid filter input given')
        return redirect(url_for('cereal.list'))

@cereal.route('/list/add')
@login_required
def add():
    """
    Get request function for loading the add cereal webpage, requires login
    """
    df = pd.read_sql("SELECT * FROM cereal", db.engine).iloc[:,1:-1]
    mfrVals = df['mfr'].unique()
    typeVals = df['type'].unique()
    return render_template('add.html', headers = df.to_dict().keys(), mfrvals = mfrVals, typevals = typeVals, new = True )

@cereal.route('/list/add',methods = ['POST'])
@login_required
def add_post():
    """
    Post request function for when user presses add on the add subpage on the webpage, requires login
    """
    try:
        #Fill values of cereal from input values, if any input value is not filled with correct value it fails
        cereal = Cereal()
        for (col,val) in request.form.items():
            set_cereal_value(col,val,cereal)
        cereal.picture = ""
        db.session.add(cereal)
        db.session.commit()
    except ValueError:
        flash("Invalid input given for one or more fields")
    return redirect(url_for('cereal.list'))


@cereal.route('/list/update/<string:id>')
@login_required
def update(id):
    """
    Get function for displaying the update page for the user, requires login.
    Queries the data of the given ID and forwards it to the html page renderer to autofil fields for user of existing data
    """
    #Hack to just get this finished fast, ideally it wouldnt be <id>?id=<id> in the url
    id = id.split('?')
    id = int(id[0])
    #Get specific ID Cereal 
    df = pd.read_sql("SELECT * FROM cereal", db.engine).iloc[:,:-1]
    #Get possible values of mfr/type
    mfrVals = df['mfr'].unique()
    typeVals = df['type'].unique()
    df = df.loc[df['id'] == id]

    if df.empty:
        flash("Update page for requested item dosent exist")
        return redirect(url_for('cereal.list'))
    #Get the specific cereal we need
    df = df.loc[df['id'] == id]
    #Get headers and data from the dataframe and display on webpage
    cerealdata =df.iloc[0].to_dict()
    return render_template('update.html', data = cerealdata, mfrvals = mfrVals,typevals = typeVals)

@cereal.route('/list/update',methods = ['POST'])
@login_required
def update_post():
    """
    Post request function for when user presses update in the update page. Checks if the item exists again 
    Requires login
    """
    try:
        #Find the item in database to update
        cereal = Cereal.query.filter_by(id=int(request.form.get('id'))).first()
        #Check if cereal exists, someone could delete during edit
        if cereal == None:
            flash('Update failed, item deleted')
            return redirect(url_for('cereal.list'))
        #Update all values even if they are unchanged, 
        for (col,val) in request.form.items():
            set_cereal_value(col,val,cereal)
        db.session.commit()
    except ValueError:
        flash("Input error on one or more fields")
    except Exception:
        flash("Unknown error occured")
    return redirect(url_for('cereal.list'))




@cereal.route('/import')
def import_data():
    #Function exist purely for importing data into database, TODO: Fix the docker import script to properly import when creating DB first time
    with open('cereals.csv') as f:
        for line in f.readlines()[1:]:
            args = line.split(',')
            newCereal = Cereal(name=args[0],mfr=args[1],type=args[2],calories=args[3],protein=args[4],fat=args[5],sodium=args[6],fiber=args[7],carbo=args[8],sugars=args[9],potass=args[10],vitamins=args[11],shelf=args[12],weight=args[13],cups=args[14],rating=args[15],picture=args[16].rstrip())
            db.session.add(newCereal)
    db.session.commit()
    return "correct"

