from flask import Blueprint, render_template, current_app,request,flash,jsonify,abort,current_app
from flask.helpers import send_from_directory, url_for
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect
from . import db
import pandas as pd
from .models import Cereal
from .helperfuncs import get_value, set_cereal_value
from flask_httpauth import HTTPBasicAuth
import re
from .models import User

"""
API blueprint file, all functions related to the /api/ part of the webpage are placed in this file.
"""

api = Blueprint('api', __name__)


authApi = HTTPBasicAuth()
@authApi.verify_password
def verify_password(username, password):
    """
    Using httpbasicauth as the normal login system does not work for the api request part. Checks if the user exist in database and the password is correct.
    """
    user = User.query.filter_by(name=username).first()
    if user and check_password_hash(user.pwd, password):
        return username


@api.route('/api/cereals/',methods = ['GET'])
def apiCereals():
    """
    Get request endpoint that returns all cereal products from database as json with 200 status code
    """
    df = pd.read_sql("SELECT * FROM cereal", db.engine).iloc[:,:-1]
    return jsonify(df.to_dict('index')), 200

@api.route('/api/cereals/<int:id>',methods = ['GET'])
def apiCereasId(id):
    """
    Get request endpoint with specific id integer value that 
    returns cereal json of the specified id, if id dosent exist it returns nothing with 204 status code
    """
    df = pd.read_sql("SELECT * FROM cereal WHERE id = %s" % id, db.engine).iloc[:,:-1]
    if not df.empty:
        return jsonify(df.to_dict('records')), 200
    else:
        return "", 204

@api.route('/api/cereals/filter',methods = ['GET'])
def apiFilterCereals():
    """
    Get request for filtering the cereal database. A filter request is a get request of key,value pair. The key is the column and value is a string with 
    the operator being the first(and second if a <= type operator) character, and the remaining chars of the string being the value being filtered at
    Returns json with the cereals that furfils the filters with a 200 status code on success
    Returns nothing and 400 bad argument if ill formed request
    """

    #Checks for the pattern "<>!=" as the first char and an optional = afterwards and stores is in group 1. While == is accepted there is not a valid request
    #The second part checks for any word pattern to follow and is stored in group 2
    prog = re.compile(r'([<>!=]=?)([ -%,.\w]+)')
    filters = request.args
    df = pd.read_sql("SELECT * FROM cereal", db.engine).iloc[:,:-1]
    try:
        for (col,val) in filters.items():
            
            #Match the result get the 2 groups 
            res = prog.match(val)
            op = res.group(1)
            value = res.group(2)
            #Translate the value to its proper type to make it compatable for pandas function
            value = get_value(col,value)
            if op == '<':
                df = df.loc[df[col] < value] 
            elif op == '>':
                df = df.loc[df[col] > value] 
            elif op == '<=':
                df = df.loc[df[col] <= value] 
            elif op == '>=':
                df = df.loc[df[col] >= value] 
            elif op == '!=':
                df = df.loc[df[col] != value] 
            elif op == '=':
                df = df.loc[df[col] == value] 
            #The regex accepts it but technically not considered a valid request
            elif op == '==':
                return "", 400
        return jsonify(df.to_dict('index')), 200
    except Exception as e:
        return "", 400

@api.route('/api/cereals/getimage/<int:id>',methods = ['GET'])
def apiGetImage(id):
    """
    GET request for getting a image, returns the image from a given id, and 404 on no file
    """
    try:
        df = pd.read_sql("SELECT * FROM cereal WHERE id = %s" %id, db.engine)
        #image loc is in the last column of the database
        filename = df.iloc[0,-1]
        return send_from_directory('static', path=filename, as_attachment=True), 200
    except:
        return abort(404)
        
@api.route('/api/cereals/delete/<int:cid>',methods = ['DELETE'])
@authApi.login_required
def delete(cid):
    """
    DELETE request, deletes the given ID. Returns 200 on success and 204 if invalid ID. Requires user auth
    """
    #Get cereal from database
    cereal = Cereal.query.filter_by(id = cid)
    if cereal == None:
        return "",204

    #Delete and commit if it exist
    cereal.delete()
    db.session.commit()
    return "",200




@api.route('/api/cereals/add/', methods=['POST'])
@authApi.login_required
def addCereal():
    """
    POST request to add cereal to the database, the post data is a json containing the various fields of a cereal and their values.
    Requires user login info in the request
    returns 200 on successfull add and 400 if ill formed request
    """
    json = request.get_json()
    try:
        #Helper function to help translate cereal from json to a Cereal object
        cereal = Cereal()
        for (col,val) in json.items():
            set_cereal_value(col,val,cereal)
        db.session.add(cereal)
        db.session.commit()
        return "",200
    except Exception as e:
        return "",400
    

   
@api.route('/api/cereals/add/<int:id>', methods=['POST'])
@authApi.login_required
def updateCereal(id):
    """
    POST request to update cereal to the database, if the id exist the cereal is updated with the new values. If the id dosent exist an error is given
    the post data is a json containing the various fields of a cereal and their values
    returns 200 on successfull update and 400 if ill formed request or the id dosent exist
    """
    cereal = Cereal.query.filter_by(id=id).first()
    #Check if cereal exists, it is not allowed to edit an not existing id
    if cereal == None:
        return "",400
    json = request.get_json()
    try:
        for (col,val) in json.items():
            set_cereal_value(col,val,cereal)
        db.session.add(cereal)
        db.session.commit()
        return "",200
    except:
        return "",400
