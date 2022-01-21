import os
from flask import current_app
from werkzeug.utils import secure_filename

from .errors import FilterError
from .constants import ALLOWED_VALUES


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
        ValueError: if a value is incorrect datatype or column header dosent exist or trying to alter id
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

def get_cereal_value(cereal):
    """
    Function that takes a cereal object and retrieves the fields.
    args:
        cereal: Cereal object
    returns:
        Array: Array of the cereal values, order is according to the constant CEREAL_HEADERS_WITH_ID
    throws:
        ValueError: if a value is incorrect datatype or column header dosent exist
    """

    values = [cereal.id, cereal.name, cereal.mfr, cereal.type, cereal.calories, cereal.protein,
              cereal.fat,cereal.sodium, cereal.fiber, cereal.carbo, cereal.sugars, cereal.potass, 
              cereal.vitamins, cereal.shelf, cereal.weight, cereal.cups, cereal.rating]
    return values
    
    

def upload_file_func(file,allowed_extensions):
    """
    Checks if a file is of an allowed extension type and saves it to the static location
    args:
        file: File object uploaded
    returns:
        filename: name of the file being uploaded
    throws:
        TypeError: If file extension is not allowed
    """
    
    def allowed_file(filename,allowed_extensions):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in allowed_extensions

    if file and allowed_file(file.filename,allowed_extensions):
        filename = secure_filename(file.filename)
        file.save(get_static_path(filename))
        return filename
    raise TypeError


def get_static_path(filename):
    """
    Returns the filepath for a given
    """
    return os.path.join(current_app.static_folder, filename)

def check_valid_filter_numbers(filter,value,args):
    """
    Function that checks if a number is reachable given a filter
    args:
        filter: string of the filter being checked
        value: value of the filter
        args: List of [min_val(number),max_val(number),not_allowed(List of number not allowed)]
    returns:
        Updated list of args
    throws:
        FilterError: If the filter will not result in any results in the given range of numbers
    """
    min_val = args[0]
    max_val = args[1]
    not_allowed = args[2]
    if filter == 'less':
        max_val = value-1
    if filter == 'lesseq':
        max_val = value
    elif filter == 'greater':
        min_val = value+1
    elif filter == 'greatereq':
        min_val = value
    elif filter == 'eq':
        if value >= min_val and value <= max_val:
            min_val = value
            max_val = value
        else:
            raise FilterError()
    elif filter == 'noteq':
        not_allowed.append(value)
    if min_val > max_val:
        raise FilterError()
    for i in range(min_val,max_val+1):
        if i not in not_allowed:
            return [min_val,max_val,not_allowed]
    raise FilterError()

def check_valid_filter_strings(filter,value,args):
    """
    Function that checks if a string is reachable given a filter
    args:
        filter: string of the filter being checked
        value: value of the filter
        args: List of [allowed(string),not_allowed(List of strings not allowed)]
    returns:
        Updated list of args
    throws:
        FilterError: If the filter will not result in any results in the given string arguments
    """
    allowed = args[0]
    not_allowed = args[1]
    if filter == 'eq':
        if value in not_allowed or allowed != '':
            raise FilterError()
        allowed = value
    elif filter == 'noteq':
        if allowed == value:
            raise FilterError()
        not_allowed.append(value)
    return [allowed,not_allowed]


def check_valid_filter(column_name,args,filter,value):
    """
    Function that checks if a filter will compute given a set of allowed input
    args:
        column_name: String of the name of the column name, must be one in CEREAL_HEADERS_WITH_ID
        args: List of arguments, 
            for ints and floats its [min_val(integer),max_val(integer),not_allowed(list of integers not allowed)]
            for strings its [allowed(string),not_allowed(list of strings)]
        filter: string of the filter type
        value: value of the filter being checked towards
    returns:
        List of updated arg arguments of same type as args
    throws:
        FilterError: If filter cant be run
    """
    column_types = {'name' : check_valid_filter_strings, 'mfr' : check_valid_filter_strings, 'calories' : check_valid_filter_numbers, 'carbo' : check_valid_filter_strings, 
                            'cups' : check_valid_filter_numbers, 'fat' : check_valid_filter_numbers, 'fiber' : check_valid_filter_numbers, 'potass' : check_valid_filter_numbers, 
                            'protein' : check_valid_filter_numbers, 'rating' : check_valid_filter_numbers, 'shelf' : check_valid_filter_numbers, 'sodium' : check_valid_filter_numbers, 
                            'sugars' : check_valid_filter_numbers, 'type' : check_valid_filter_numbers, 'vitamins' : check_valid_filter_numbers, 'weight' : check_valid_filter_numbers,
                            'id' : check_valid_filter_numbers}
    func = column_types[column_name]
    return func(filter,value,args)

