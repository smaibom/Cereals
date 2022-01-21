from flask import Blueprint, render_template, request,flash,current_app
from flask.helpers import url_for
from flask_login import login_required
from werkzeug.utils import redirect

from .errors import FilterError
from .. import db
from .models import Cereal,CerealPicture
import pandas as pd
from .helperfuncs import change_to_column_type, check_valid_filter, get_static_path, upload_file_func
from .constants import ALLOWED_DATA_EXTENSIONS, ALLOWED_IMAGE_EXTENSIONS, ALLOWED_MFR, ALLOWED_TYPES, CEREAL_HEADERS_WITH_ID, CEREAL_HEADERS_WITHOUT_ID, FILTER_OPERATORS
from .dbfunctions import db_add_cereal, db_add_cereal_imagepath, db_bulk_add_cereal, db_delete_cereal, db_get_all_cereals_as_df,  db_get_cereal_imagepath, db_get_id_cereal_as_df, db_update_cereal, db_update_cereal_imagepath
"""
Cereal blueprint functions are placed here
"""

cereal = Blueprint('cereal', __name__)

@cereal.route('/list')
def list():
    #Get all cereals in database
    df = db_get_all_cereals_as_df()

    #Get headers and data from the dataframe and display on webpage
    cerealdata =df.to_dict('index')
    return render_template('cereals.html', cereals = cerealdata, headers = CEREAL_HEADERS_WITH_ID, operators = FILTER_OPERATORS )

@cereal.route('/list/<int:id>')
def list_with_id(id):
    """
    Get request function for listing specific cereals
    """
    #Get specific ID Cereal 
    try:
        df = db_get_id_cereal_as_df(id)
    except LookupError:
        #If ID dosent exist
        flash('Requested cereal ID dosent exists')
        return redirect(url_for('cereal.list'))
    
    #Get image, if no imagepath is set we set to default image
    try:
        imagepath = db_get_cereal_imagepath(id)
        image = url_for('static', filename = imagepath)
    except LookupError:
        #If imagepath dosent exist
        image = url_for('static', filename = 'default.png')

    #Pass data along to template
    return render_template('cereal.html', cereals = df.to_dict(), headers = CEREAL_HEADERS_WITH_ID, id = id, image = image)

@cereal.route('/list/delete',methods = ["POST"])
@login_required
def delete_with_id():
    """
    Function for deleting cereal IDs when user presses delte in the specific cereal page, this is a POST request as html tags only allow GET and POST
    requires login
    """
    #We get the ID from the post request and delete it and redirect back to list view
    try:
        id = request.form.get('id')
        if db_delete_cereal(id):
            flash("Cereal deleted")
        else:
            flash("Cereal not deleted")
    except LookupError:
        flash('cereal dosent exist')
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

    df = db_get_all_cereals_as_df()
    prevFilters = []
    filters = dict()
    try:
        #Make value into correct datatype for filtering
        for i in range(len(field)):
            curField = field[i]
            curValue = change_to_column_type(curField,value[i])
            curOp = op[i]
            prevFilters.append((curField,curOp,curValue))
            curOp = FILTER_OPERATORS[curOp]

            
            #Check for if filters can produce a result for the user
            if curField in filters:
                args = filters[curField]
            else:
                #If a filter for a given column havent been encounted yet we create the args for the function
                if type(curValue) == int or type(curValue) == float:
                    #Set initial min,max vals.
                    min_val = 0
                    max_val = float('inf')
                    not_allowed = []
                    #Package the arguments to an argument array
                    args = [min_val,max_val,not_allowed]
                else:
                    #Set initial allowed to nothing
                    allowed = ''
                    not_allowed = []
                    #Package the arguments to an argument array
                    args = [allowed,not_allowed]

            filters[curField] = check_valid_filter(curField,args,curOp,curValue)
            
            if curOp == '=':
                df = df.loc[df[curField] == curValue] 
            elif curOp == '!=':
                df = df.loc[df[curField] != curValue]   
            elif curOp == '>':
                df = df.loc[df[curField] > curValue] 
            elif curOp == '<':
                df = df.loc[df[curField] < curValue] 
            elif curOp == '<=':
                df = df.loc[df[curField] <= curValue] 
            elif curOp == '>=':
                df = df.loc[df[curField] >= curValue] 
            
        cerealdata =df.to_dict('index')
        return render_template('cereals.html', cereals = cerealdata, headers = CEREAL_HEADERS_WITH_ID,  operators = FILTER_OPERATORS, prevFilters = prevFilters)
    except FilterError:
        flash('Filters would never give a result')
        return redirect(url_for('cereal.list'))
    except Exception as e:
        flash('invalid filter input given')
        print(e)
        return redirect(url_for('cereal.list'))


@cereal.route('/list/add')
@login_required
def add():
    """
    Get request function for loading the add cereal webpage, requires login
    """
    return render_template('add.html', headers = CEREAL_HEADERS_WITHOUT_ID, mfrvals = ALLOWED_MFR, typevals = ALLOWED_TYPES, new = True )




@cereal.route('/list/add',methods = ['POST'])
@login_required
def add_post():
    """
    Post request function for when user presses add on the add subpage on the webpage, requires login
    """
    try:
        if db_add_cereal(request.form):
            flash('Added cereal to DB')
        else:
            flash("Cereal not added to DB")
    except ValueError:
        flash('Invalid input given')
        return redirect(url_for('cereal.add_post'))
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
    try:
        df = db_get_id_cereal_as_df(id)
        return render_template('update.html', data = df.iloc[0].to_dict(), mfrvals = ALLOWED_MFR ,typevals = ALLOWED_TYPES)
    except LookupError:
        flash("Update page for requested item dosent exist")
        return redirect(url_for('cereal.list'))


@cereal.route('/list/update',methods = ['POST'])
@login_required
def update_post():
    """
    Post request function for when user presses update in the update page. Checks if the item exists again 
    Requires login
    """
    try:
        #Find the item in database to update
        id = int(request.form.get('id'))
        if db_update_cereal(id,request.form):
            flash("%s successfully updated" % id)
    except ValueError:
        flash("Input error on one or more fields")
        return redirect(url_for('cereal.update',id = '%s?' % id))
    except KeyError:
        #Tried to set a column that dosent exist
        pass
    except LookupError:
        flash('Cereal does not exist')
    return redirect(url_for('cereal.list'))

@cereal.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """
    Post function for uploading file, currently can upload a file with no attached cereal to it
    Requires login
    """

    id = int(request.form.get('id'))
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('cereal.list_with_id', id=int(id)))

    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('cereal.list_with_id', id=int(id)))
    
    #Upload file
    try:
        filename = upload_file_func(file,ALLOWED_IMAGE_EXTENSIONS)
        current_app.logger.info('Picture %s uploaded' %filename)
    except TypeError:
        flash('File not allowed format')
        return redirect(url_for('cereal.list_with_id', id=int(id)))

    #Update DB with path to image
    try:
        picture = db_get_cereal_imagepath(id)
        if db_update_cereal_imagepath(id,filename):
            flash('updated image successfully')
        else:
            flash('Image not updated')
    #Check if picture exist
    except LookupError:
        try:
            if db_add_cereal_imagepath(id,filename):
                flash('image added successfully')
            else:
                flash('Image not updated')
        #Check if cereal the picture is added to exists
        except LookupError:
            flash('Cereal does not exist anymore')
            return redirect(url_for('cereal.list'))
    
    return redirect(url_for('cereal.list_with_id', id=int(id)))

@cereal.route('/importcsv')
@login_required
def import_csv():
    return render_template('uploadcsv.html')
    

@cereal.route('/importcsv', methods=['POST'])
@login_required
def import_csv_post():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('cereal.import_csv'))

    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('cereal.import_csv'))
    #Upload file
    try:
        filename = upload_file_func(file,ALLOWED_DATA_EXTENSIONS)
        current_app.logger.info('Uploaded %s for data import' %filename)
    except TypeError:
        flash('File not allowed format')
        return redirect(url_for('cereal.import_csv'))
    try:
        filename = get_static_path(filename)
        df = pd.read_csv(filename,usecols=CEREAL_HEADERS_WITHOUT_ID).to_dict('records')
    except FileNotFoundError:
        flash('error reading file')
        return redirect(url_for('cereal.import_csv'))
    amount_uploaded = db_bulk_add_cereal(df)
    flash('Uploaded csv to DB, added %d cereals' %amount_uploaded)
    return redirect(url_for('cereal.list'))

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