ALLOWED_IMAGE_EXTENSIONS = {'jfif', 'png', 'jpg', 'jpeg'}
ALLOWED_DATA_EXTENSIONS = {'csv'}
ALLOWED_TYPES = {'C', 'H'}
ALLOWED_MFR = {'Q','K','R','G','P','N','A'}
CEREAL_HEADERS_WITH_ID = ['id', 'name', 'mfr', 'type', 'calories', 'protein', 'fat', 'sodium', 
                          'fiber', 'carbo', 'sugars', 'potass', 'vitamins', 'shelf', 'weight', 'cups', 'rating']
CEREAL_HEADERS_WITHOUT_ID = ['name', 'mfr', 'type', 'calories', 'protein', 'fat', 'sodium', 'fiber', 'carbo',
                             'sugars', 'potass', 'vitamins', 'shelf', 'weight', 'cups', 'rating']
FILTER_OPERATORS = {'eq' : '=', 'noteq' : '!=', 'less' : '<', 'greater' : '>', 'lesseq' : '<=', 'greatereq' : '>=' }
ALLOWED_VALUES = {'name' : None, 'mfr' : ALLOWED_MFR, 'type' : ALLOWED_TYPES, 'calories' : None, 'protein' : None, 'fat' : None,
                  'sodium' : None, 'fiber' : None,  'carbo' : None, 'sugars' : None, 'potass': None, 'vitamins' : None, 'shelf' : None,
                   'shelf' : None, 'weight' : None, 'cups' : None, 'rating': None, 'id': None}
