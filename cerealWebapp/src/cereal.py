from flask import Blueprint, render_template, request,flash
from flask.helpers import url_for
from flask_login import login_required
from werkzeug.utils import redirect
from .. import db
import pandas as pd
from .models import Cereal,CerealPicture
from .helperfuncs import change_to_column_type, set_cereal_value, upload_file_func
import pyodbc
from .constants import ALLOWED_MFR, ALLOWED_TYPES, CEREAL_HEADERS_WITH_ID, CEREAL_HEADERS_WITHOUT_ID

"""
Cereal blueprint functions are placed here

TODO: Move pictures to own table, use foreign key relation to link to main table
"""

cereal = Blueprint('cereal', __name__)

@cereal.route('/list')
def list():
    #Get all cereals in database
    df = pd.read_sql("SELECT * FROM cereal", db.engine)
    #Get headers and data from the dataframe and display on webpage
    cerealdata =df.to_dict('index')
    return render_template('cereals.html', cereals = cerealdata, headers = CEREAL_HEADERS_WITH_ID )

@cereal.route('/list/<int:id>')
def list_with_id(id):
    #Get specific ID Cereal 
    df = pd.read_sql("SELECT * FROM cereal WHERE id = %s" %id, db.engine)
    if df.empty:
        flash('Requested cereal ID dosent exists')
        return redirect(url_for('cereal.list'))
    dfImage = pd.read_sql("SELECT picturepath FROM cerealpictures WHERE cerealid = %s" %id, db.engine)
    if dfImage.empty:
        image = url_for('static', filename = 'default.png')
    else:
        imagePath = dfImage.iloc[0,0]
        image = url_for('static', filename = imagePath)
    #Get headers and data from the dataframe and display on webpage
    cerealdata =df.to_dict()
    return render_template('cereal.html', cereals = cerealdata, headers = CEREAL_HEADERS_WITH_ID, id = id, image = image)

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
    field = request.form.getlist('field')
    op = request.form.getlist('op')
    value = request.form.getlist('value')

    #Get entire cereals
    df = pd.read_sql("SELECT * FROM cereal", db.engine)
    try:
        #Make value into correct datatype for filtering
        for i in range(len(field)):
            print("test")
            curField = field[i]
            curValue = change_to_column_type(curField,value[i])
            curOp = op[i]
            if curOp == 'eq':
                df = df.loc[df[curField] == curValue] 
            elif curOp == 'noteq':
                df = df.loc[df[curField] != curValue]   
            elif curOp == 'greater':
                df = df.loc[df[curField] > curValue] 
            elif curOp == 'less':
                df = df.loc[df[curField] < curValue] 
            elif curOp == 'lesseq':
                df = df.loc[df[curField] <= curValue] 
            elif curOp == 'greatereq':
                df = df.loc[df[curField] >= curValue] 
        cerealdata =df.to_dict('index')
        return render_template('cereals.html', cereals = cerealdata, headers = CEREAL_HEADERS_WITH_ID, fields = field, ops = op, values = value )
    except:
        flash('invalid filter input given')
        return redirect(url_for('cereal.list'))

@cereal.route('/list/add')
@login_required
def add():
    """
    Get request function for loading the add cereal webpage, requires login
    """
    mfrVals = ALLOWED_MFR
    typeVals = ALLOWED_TYPES
    return render_template('add.html', headers = CEREAL_HEADERS_WITHOUT_ID, mfrvals = mfrVals, typevals = typeVals, new = True )




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
    df = pd.read_sql("SELECT * FROM cereal WHERE id = %d" % id, db.engine)
    #Get possible values of mfr/type
    mfrVals = ALLOWED_MFR
    typeVals = ALLOWED_TYPES

    if df.empty:
        flash("Update page for requested item dosent exist")
        return redirect(url_for('cereal.list'))
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

@cereal.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """
    Post function for uploading file
    Requires login
    """
    id = int(request.form.get('id'))
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('list_spec_cereal', id=int(id)))
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('list_spec_cereal', id=int(id)))
    try:
        filename = upload_file_func(file)
        picture = CerealPicture.query.filter_by(cerealid=id).first()
        #New entry, dosent exist createone
        if picture != None:
            picture.picturepath = filename
        else:
            cereal = Cereal.query.filter_by(id=id).first()
            picture = CerealPicture(cerealid = cereal.id, picturepath = filename)
            db.session.add(picture)
        db.session.commit()
        return redirect(url_for('list_spec_cereal', id=int(id)))

    except TypeError:
        flash('File not allowed format')
        return redirect(url_for('list_spec_cereal', id=int(id)))




@cereal.route('/import')
def import_data():
    #Function exist purely for importing data into database, TODO: Fix the docker import script to properly import when creating DB first time
    with open('cereals.csv') as f:
        for line in f.readlines()[1:]:
            args = line.split(',')
            newCereal = Cereal(name=args[0],mfr=args[1],type=args[2],calories=args[3],protein=args[4],fat=args[5],sodium=args[6],fiber=args[7],carbo=args[8],sugars=args[9],potass=args[10],vitamins=args[11],shelf=args[12],weight=args[13],cups=args[14],rating=args[15])
            db.session.add(newCereal)
            db.session.flush()
            newPicture = CerealPicture(cerealid = newCereal.id,picturepath = args[16].rstrip())
            db.session.add(newPicture)
            db.session.flush()

        db.session.commit()
    return "correct"

