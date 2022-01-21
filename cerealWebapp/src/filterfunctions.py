from .errors import FilterError, OperatorNotFoundError

"""
Functions for filtering goes here, contains functions for basic filtering and validation if a list of filters can produce a result
"""

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
    if filter == '<':
        max_val = min(value-1,max_val)
    if filter == '<=':
        max_val = min(value,max_val)
    elif filter == '>':
        min_val = max(value+1,min_val)
    elif filter == '>=':
        min_val = max(value,max_val)
    elif filter == '=':
        if value >= min_val and value <= max_val:
            min_val = value
            max_val = value
        else:
            raise FilterError()
    elif filter == '!=':
        not_allowed.append(value)
    if min_val > max_val:
        raise FilterError()
    i = min_val
    while i <= max_val:
        if i not in not_allowed:
            return [min_val,max_val,not_allowed]
        i += 1
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
    if filter == '=':
        if value in not_allowed or allowed != '':
            raise FilterError()
        allowed = value
    elif filter == '!=':
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

def check_valid_filters(args):
    """
    Checks if a list of filters can produce a result in any circumstance. This is not relative to a dataset and used to check if a result could be found
    args:
        args: List of tuples with 
            column: String of the name of the column being filtered
            op: String of the operator for the filter, must be in FILTER_OPERATORS
            value: Value for the filter 
    returns:
        True if a result could be found after filtering
        False if no result could ever be found for one or more columns
    """
    filters = dict()
    try:
        for (column,op,value) in args:
            #Check for if filter for a column has been encountered before
            if column in filters:
                args = filters[column]
            else:
                #If a filter for a given column havent been encounted yet we create the args for the function
                if type(value) == int or type(value) == float:
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
            filters[column] = check_valid_filter(column,args,op,value)
        return True
    except FilterError:
        return False


def filter_cereals(df,args):
    """
    Takes a dataframe and performs a list of filters on it
    args:
        df: DataFrame with the cereal data
        args: List of tuples with 
            column: String of the name of the column being filtered
            op: String of the operator for the filter, must be in FILTER_OPERATORS
            value: Value for the filter 
        returns:
            df: Filtered dataframe of all the filters
        throws:
            OperatorNotFoundError: If the operator does not exist
    """
    for (column,op,value) in args:
        if op == '=':
            df = df.loc[df[column] == value] 
        elif op == '!=':
            df = df.loc[df[column] != value]   
        elif op == '>':
            df = df.loc[df[column] > value] 
        elif op == '<':
            df = df.loc[df[column] < value] 
        elif op == '<=':
            df = df.loc[df[column] <= value] 
        elif op == '>=':
            df = df.loc[df[column] >= value] 
        else:
            raise OperatorNotFoundError()
    return df


