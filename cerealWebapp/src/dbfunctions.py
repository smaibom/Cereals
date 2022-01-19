from flask import current_app
from .helperfuncs import set_cereal_value
from .. import db
from .models import Cereal, CerealPicture
import pandas as pd
import sqlalchemy

def db_get_all_as_df():
    pass

def db_get_as_df(sql):
    """
    """
    try:
        df = pd.read_sql(sql, db.engine)
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
        False: On failure
    """
    try:
        Cereal.query.filter(Cereal.id == id).delete()
        db.session.commit()
        current_app.logger.info('Deleted cereal id %s from database' % id)
        return True
    except sqlalchemy.exc.OperationalError:
        current_app.logger.critical('DB Error occured when getting cereal image')
        return False

def db_add_cereal(input_dict):
    try:
        cereal = Cereal()
        for (col,val) in input_dict.items():
            set_cereal_value(col,val,cereal)
        cereal.picture = ""
        db.session.add(cereal)
        db.session.commit()
        current_app.logger.info('Added new cereal to DB')
        return True
    except sqlalchemy.exc.OperationalError:
        current_app.logger.critical('DB Error occured when getting cereal image')
        return False
    except ValueError:
        return False

def db_update_cereal(id,input_dict):
    try:
        cereal = Cereal.query.filter_by(id=id).first()
        #Check if cereal exists, someone could delete during edit
        if cereal == None:
            raise LookupError
        #Update all values even if they are unchanged, 
        for (col,val) in input_dict.items():
            set_cereal_value(col,val,cereal)
        db.session.commit()
        current_app.logger.info('Updated cereal id %s' % id)
        return True
    except sqlalchemy.exc.OperationalError:
        current_app.logger.critical('DB Error occured when getting cereal image')
        return False


def db_get_cereal_imagepath(id):
    try:
        picture = CerealPicture.query.filter_by(cerealid=id).first()
        #Check if picture exists
        if picture != None:
            return picture.picturepath
        return None
    except sqlalchemy.exc.OperationalError:
        current_app.logger.critical('DB Error occured when getting cereal image')

def db_add_cereal_imagepath(cereal_id,filename):
    try:
        #We need the cereal to add foreign key relation
        cereal = Cereal.query.filter_by(id=cereal_id).first()

        #Check if cereal exist, might have been deleted
        if not cereal:
            raise LookupError
        
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
    try:
        #Query the existing picture location
        cereal_picture = CerealPicture.query.filter_by(cerealid=cereal_id).first()

        #Check if cereal exist, might have been deleted, if cereal is deleted it cascades into cerealpicture
        if not cereal_picture:
            raise LookupError

        #Update picturepath
        cereal_picture.picturepath = filename
        db.session.commit()

        current_app.logger.info('Picturepath %s for cerealid %s updated' % (filename,cereal_id))
        return True

    except sqlalchemy.exc.OperationalError:
        current_app.logger.critical('DB Error occured when updating cereal image')
        return False