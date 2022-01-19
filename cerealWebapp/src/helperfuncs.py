import os
from flask import current_app
from werkzeug.utils import secure_filename
from .constants import ALLOWED_EXTENSIONS, ALLOWED_VALUES

"""
Helper functions used in multiple files go here
"""

def change_to_column_type(column,value):
    """
    Takes a column type for a cereal and changes the value into the proper datatype
    args:
        column: String value of the column header name
        value: String value of input to be changed to its desired datatype
    returns:
        value of its desired datatype
    throws:
        ValueError if value is not changeable into desired datatype
    """
    def check_int(value,constaints):
        result_val = int(value) 
        return result_val

    def check_float(value,constraints):
        return float(value)

    def check_string(value,constaints):
        if len(value) > 0:
            return value
        raise ValueError()
    
    def check_char(value,constraints):
        if len(value) > 0 and value in constraints:
            return value
        raise ValueError()


    column_types = {'name' : check_string, 'mfr' : check_char, 'calories' : check_int, 'carbo' : check_float, 
                            'cups' : check_float, 'fat' : check_int, 'fiber' : check_float, 'potass' : check_int, 
                            'protein' : check_int, 'rating' : check_int, 'shelf' : check_int, 'sodium' : check_int, 
                            'sugars' : check_int, 'type' : check_char, 'vitamins' : check_int, 'weight' : check_float,
                            'id' : check_int}
    #Look up function to translate datatype
    check_function = column_types[column]
    allowed_values = ALLOWED_VALUES[column]
    result = check_function(value,allowed_values)
    return result


def set_cereal_value(col,value,cereal):
    """
    Function that takes a cereal object and changes the field of a given column to the given value. 
    args:
        col: String of the column header
        value: String of the value
        cereal: Cereal object where the fields should be changed
    throws:
        ValueError: if a value is incorrect datatype or column header dosent exist
    """

    #Set fields
    try:
        if col == 'name':
            cereal.name = change_to_column_type(col,value)
        elif col == 'mfr':
            cereal.mfr =  change_to_column_type(col,value)
        elif col == 'calories':
            cereal.calories = change_to_column_type(col,value)
        elif col == 'carbo':
            cereal.carbo = change_to_column_type(col,value)
        elif col == 'cups':
            cereal.cups = change_to_column_type(col,value)
        elif col == 'fat':
            cereal.fat = change_to_column_type(col,value)
        elif col == 'fiber':
            cereal.fiber = change_to_column_type(col,value)
        elif col == 'potass':
            cereal.potass = change_to_column_type(col,value)
        elif col == 'protein':
            cereal.protein = change_to_column_type(col,value)
        elif col == 'rating':
            cereal.rating = change_to_column_type(col,value)
        elif col == 'shelf':
            cereal.shelf = change_to_column_type(col,value)
        elif col == 'sodium':
            cereal.sodium = change_to_column_type(col,value)
        elif col == 'sugars':
            cereal.sugars = change_to_column_type(col,value)
        elif col == 'type':
            cereal.type = change_to_column_type(col,value)
        elif col == 'type':
            cereal.type = change_to_column_type(col,value)
        elif col == 'vitamins':
            cereal.vitamins = change_to_column_type(col,value)
        elif col == 'weight':
            cereal.weight = change_to_column_type(col,value)
        elif col == 'id':
            #ID is immuteable
            ValueError('Dont change ID')
        else:
            raise ValueError('Invalid column')
    except (KeyError,ValueError) as e:
        raise e

    
    

def upload_file_func(file):
    """
    Checks if a file is of an allowed extension type and saves it to the static location
    args:
        file: File object uploaded
    returns:
        filename: name of the file being uploaded
    throws:
        TypeError: If file extension is not allowed
    """
    
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.static_folder, filename))
        return filename
    raise TypeError