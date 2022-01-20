from flask import Blueprint, request,jsonify,abort,current_app
from flask.helpers import send_from_directory
from werkzeug.security import check_password_hash
from .dbfunctions import db_add_cereal, db_delete_cereal, db_get_all_cereals_as_df, db_get_cereal_imagepath, db_get_id_cereal_as_df, db_update_cereal
import pandas as pd
from .models import Cereal
from .helperfuncs import change_to_column_type
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
        current_app.logger.info('%s successfully authenticated on api' % username)
        return username
    current_app.logger.info('%s failed to authenticated on api' % username)


@api.route('/api/cereals/',methods = ['GET'])
def api_get_all_cereals():
    """
    Get request endpoint that returns all cereal products from database as json with 200 status code
    """
    df = db_get_all_cereals_as_df()
    return jsonify(df.to_dict('index')), 200

@api.route('/api/cereals/<int:id>',methods = ['GET'])
def api_get_cereal_id(id):
    """
    Get request endpoint with specific id integer value that 
    returns cereal json of the specified id, if id dosent exist it returns nothing with 204 status code
    """
    try:
        df = db_get_id_cereal_as_df(id)
        return (df.iloc[0].to_dict()), 200
    except LookupError:
        return "", 204

@api.route('/api/cereals/filter',methods = ['GET'])
def api_filter_cereals():
    """
    Get request for filtering the cereal database. A filter request is a get request of key,value pair. The key is the column and value is a string with 
    the operator being the first(and second if a <= type operator) character, and the remaining chars of the string being the value being filtered at
    Returns json with the cereals that furfils the filters with a 200 status code on success
    Returns nothing and 400 bad argument if ill formed request
    """

    #Checks for the pattern "<>!=" as the first char and an optional = afterwards and stores is in group 1. While == is accepted there is not a valid request
    #The second part checks for any word pattern to follow and is stored in group 2
    prog = re.compile(r'([<>!=]=?)([ -%,.\w]+)')
    
    #Get arguments
    filters = request.args
    df = db_get_all_cereals_as_df()

    try:
        for (col,val) in filters.items():
            #Match the result get the 2 groups 
            res = prog.match(val)
            op = res.group(1)
            value = res.group(2)
            #Translate the value to its proper type to make it compatable for pandas function
            value = change_to_column_type(col,value)
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
            if df.empty:
                return "", 204
        return jsonify(df.to_dict('index')), 200
    except Exception as e:
        return "", 400

@api.route('/api/cereals/getimage/<int:id>',methods = ['GET'])
def api_get_image(id):
    """
    GET request for getting a image, returns the image from a given id, and 204 on no file
    """
    try:
        filename = db_get_cereal_imagepath(id)
        return send_from_directory('static', path=filename, as_attachment=True), 200
    except LookupError:
        return "",204
        
@api.route('/api/cereals/delete/<int:cid>',methods = ['DELETE'])
@authApi.login_required
def api_delete_cereals(cid):
    """
    DELETE request, deletes the given ID. Returns 200 on success and 204 if invalid ID. Requires user auth
    """
    try:
        if db_delete_cereal(cid):
            return "", 200
        else:
            return "", 202
    except LookupError:
        return "",204




@api.route('/api/cereals/add/', methods=['POST'])
@authApi.login_required
def api_add_cereal():
    """
    POST request to add cereal to the database, the post data is a json containing the various fields of a cereal and their values.
    Requires user login info in the request
    returns 200 on successfull add and 400 if ill formed request
    """
    json = request.get_json()
    try:
        #Helper function to help translate cereal from json to a Cereal object
        if db_add_cereal(json):
            return "",200
        else:
            return "",202
    except ValueError as e:
        return "",400
    

   
@api.route('/api/cereals/add/<int:id>', methods=['PUT'])
@authApi.login_required
def api_update_cereal(id):
    """
    POST request to update cereal to the database, if the id exist the cereal is updated with the new values. If the id dosent exist an error is given
    the post data is a json containing the various fields of a cereal and their values
    returns 200 on successfull update and 400 if ill formed request or the id dosent exist
    """
    json = request.get_json()
    try:
        db_update_cereal(id,json)
        return "",200
    except LookupError:
        return "",204
    except ValueError:
        return "",400
