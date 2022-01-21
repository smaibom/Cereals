from flask import current_app
from .constants import CEREAL_HEADERS_WITH_ID

from .helperfuncs import get_cereal_value, set_cereal_value
from .. import db
from .models import Cereal, CerealPicture, User
import pandas as pd
import sqlalchemy
"""
File for all database functions
"""


def db_get_all_cereals_as_df():
    """
    Returns all entries from cereal table into a pandas dataframe
    returns:
        Pandas Dataframe with all cereal values from DB
    """
    sql = "SELECT * FROM cereal"
    try:
        df = pd.read_sql(sql, db.engine)
        return df
    except sqlalchemy.exc.OperationalError:
        df = pd.DataFrame([],columns=CEREAL_HEADERS_WITH_ID)
        current_app.logger.critical('DB Error occured when getting cereal data')
        return df

def db_get_id_cereal_as_df(id):
    """
    Returns a dataframe with cereal data of a given ID

    args:
        id: Integer value of the id of the cereal
    returns:
        Dataframe with the values of the given ID
    throws:
        LookupError: If id dosent exist in DB

    """
    try:
        cereal = Cereal.query.filter_by(id = id).first()
        if not cereal:
            raise LookupError('Id dosent exist')
        
        #Pandas rows is list of list, so changing it to be one
        values = [get_cereal_value(cereal)]
        df = pd.DataFrame(values,columns=CEREAL_HEADERS_WITH_ID)
        return df
    except sqlalchemy.exc.OperationalError:
        current_app.logger.critical('DB Error occured when getting cereal data')

def db_delete_cereal(id):
    """
    Deletes a cereal with a specific ID from the database
    args:
        id: int value of the cereal id being deleted
    returns:
        True: On success
        False: On DB failure
    throws:
        LookupError: If the cereal does not exist
    """
    try:
        cereal = Cereal.query.filter_by(id = id)

        #Check if it exist before we attempt to delete
        if cereal.first() == None:
            raise LookupError('Cereal does not exist')

        #Delete and commit if it exist
        cereal.delete()
        db.session.commit()
        current_app.logger.info('Deleted cereal id %s from database' % id)
        return True

    except sqlalchemy.exc.OperationalError:
        current_app.logger.critical('DB Error occured when getting cereal image')
        return False


def db_add_cereal(input_dict):
    """
    Adds a cereal to the DB
    args:
        input_dict: a dictionary with the values being added where keys are the column names
    returns:
        True: On successfull operation
        False: On DB failure
    throws:
        ValueError: If input_dict parameters are incorrect, invalid column or value types
    """
    try:
        #Create new cereal object
        cereal = Cereal()
        #Iterate over each column, value and add it to the cereal object
        for (col,val) in input_dict.items():
            set_cereal_value(col,val,cereal)

        #Add cereal object to DB and commit
        db.session.add(cereal)
        db.session.commit()
        current_app.logger.info('Added new cereal to DB')
        return True

    except sqlalchemy.exc.OperationalError:
        current_app.logger.critical('DB Error occured when getting cereal image')
        return False

    except ValueError:
        raise ValueError('Invalid input parameters')

def db_bulk_add_cereal(cereals_list):
    """
    bulk add cereal to the DB
    args:
        cereals_list: a list of dictionaries of cereal items 
    returns:
        Integer value of how many cereals from set was uploaded
    """
    try:
        number_uploaded = 0
        for cereal_item in cereals_list:
            try:
                cereal = Cereal()
                for (col,val) in cereal_item.items():
                    set_cereal_value(col,val,cereal)
                db.session.add(cereal)
                number_uploaded += 1
            except ValueError:
                pass
        db.session.commit()
        current_app.logger.info('Added %d cereals to DB' % number_uploaded)
        return number_uploaded
    except sqlalchemy.exc.OperationalError:
        current_app.logger.critical('DB Error occured when getting cereal image')
        return 0


def db_update_cereal(id,input_dict):
    """
    Updates an existing cereal object in the database
    args:
        id: Integer value of the id of the cereal being updated
        input_dict: a dictionary with the values being updated where keys are the column names
    returns:
        True: On success
        False: On DB failure
    throws:
        LookupError: If cereal does not exist
    """
    try:
        #Query the cereal in DB
        cereal = Cereal.query.filter_by(id=id).first()

        #Check if cereal exists, someone could delete during edit
        if cereal == None:
            raise LookupError
        
        #Update values and commit
        for (col,val) in input_dict.items():
            set_cereal_value(col,val,cereal)
        db.session.commit()
        current_app.logger.info('Updated cereal id %s' % id)
        return True

    except sqlalchemy.exc.OperationalError:
        current_app.logger.critical('DB Error occured when getting cereal image')
        return False


def db_get_cereal_imagepath(id):
    """
    Gets a imagepath from the database
    args:
        id: Integer value of the cereal id picture we are returning
    returns:
        Filename string if the filename exist, None on DB failure
    throws:
        LookupError: If picture entry dosent exist in DB
    """
    try:
        #Query for picture
        picture = CerealPicture.query.filter_by(cerealid=id).first()

        #Check if picture exists
        if picture == None:
            raise LookupError('No entry for cerealpicture')

        return picture.picturepath
    except sqlalchemy.exc.OperationalError:
        current_app.logger.critical('DB Error occured when getting cereal image')

def db_add_cereal_imagepath(cereal_id,filename):
    """
    Adds the path of a cereal image stored on server to the DB
    args:
        cereal_id: Integer value of the cereal id which the image is to be linked to
        filename: String value of the path to the file in the static folder
    returns:
        True: On success
        False: On DB failure
    throws:
        LookupError: If cereal does not exist
    """
    try:
        #We need the cereal to add foreign key relation
        cereal = Cereal.query.filter_by(id=cereal_id).first()

        #Check if cereal exist, might have been deleted
        if not cereal:
            raise LookupError('Attempted to add cereal picture, but the cereal no longer exist')
        
        #Add picturepath to DB
        picture = CerealPicture(cerealid = cereal.id, picturepath = filename)
        db.session.add(picture)
        db.session.commit()
        current_app.logger.info('Picturepath %s for cerealid %s added' % (filename,cereal_id))
        return True

    except sqlalchemy.exc.OperationalError:
        current_app.logger.critical('DB Error occured when updating cereal image')
        return False


def db_update_cereal_imagepath(cereal_id,filename):
    """
    Updates the filepath to an image for a given cereal
    args:
        cereal_id: Integer value of the cereal id which the image is to be linked to
        filename: String value of the path to the file in the static folder
    returns:
        True: On success
        False: On DB failure
    throws:
        LookupError: If cereal does not exist
    """
    try:
        #Query the existing picture location
        cereal_picture = CerealPicture.query.filter_by(cerealid=cereal_id).first()

        #Check if cereal exist, might have been deleted, if cereal is deleted it cascades into cerealpicture
        if not cereal_picture:
            raise LookupError('Attempted to modify cereal picture but it dosent exist in DB')

        #Update picturepath
        cereal_picture.picturepath = filename
        db.session.commit()

        current_app.logger.info('Picturepath %s for cerealid %s updated' % (filename,cereal_id))
        return True

    except sqlalchemy.exc.OperationalError:
        current_app.logger.critical('DB Error occured when updating cereal image')
        return False

