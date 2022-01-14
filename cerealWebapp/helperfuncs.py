from .models import Cereal
"""
Helper functions used in multiple files go here
"""

def get_value(column,value):
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
    def to_int(value):
        return int(value) 

    def to_float(value):
        return float(value)

    def to_string(value):
        return str(value)

    #Hardcoded dict of fucntions to match database column types
    columnTypes = {'name' : to_string, 'mfr' : to_string, 'calories' : to_int, 'carbo' : to_float, 
                            'cups' : to_float, 'fat' : to_int, 'fiber' : to_float, 'potass' : to_int, 
                            'protein' : to_int, 'rating' : to_int, 'shelf' : to_int, 'sodium' : to_int, 
                            'sugars' : to_int, 'type' : to_string, 'vitamins' : to_int, 'weight' : to_float,
                            'id' : to_int}
    try:
        #Look up function to translate datatype
        func = columnTypes[column]
        return func(value)
    except:
        raise ValueError

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
    if col == 'name':
        cereal.name = get_value(col,value)
    elif col == 'mfr':
        cereal.mfr =  get_value(col,value)
    elif col == 'calories':
        cereal.calories = get_value(col,value)
    elif col == 'carbo':
        cereal.carbo = get_value(col,value)
    elif col == 'cups':
        cereal.cups = get_value(col,value)
    elif col == 'fat':
        cereal.fat = get_value(col,value)
    elif col == 'fiber':
        cereal.fiber = get_value(col,value)
    elif col == 'potass':
        cereal.potass = get_value(col,value)
    elif col == 'protein':
        cereal.protein = get_value(col,value)
    elif col == 'rating':
        cereal.rating = get_value(col,value)
    elif col == 'shelf':
        cereal.shelf = get_value(col,value)
    elif col == 'sodium':
        cereal.sodium = get_value(col,value)
    elif col == 'sugars':
        cereal.sugars = get_value(col,value)
    elif col == 'type':
        cereal.type = get_value(col,value)
    elif col == 'type':
        cereal.type = get_value(col,value)
    elif col == 'vitamins':
        cereal.vitamins = get_value(col,value)
    elif col == 'weight':
        cereal.weight = get_value(col,value)
    elif col == 'id':
        #ID is immuteable
        pass
    else:
        raise ValueError('Invalid column')
    