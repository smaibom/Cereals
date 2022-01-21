#Allowed extensions for file uploads for cereals pictures
ALLOWED_IMAGE_EXTENSIONS = {'jfif', 'png', 'jpg', 'jpeg'}
#Allowed extensions for bulk upload of new entries
ALLOWED_DATA_EXTENSIONS = {'csv'}
#The valid strings for the "types" field in the cereal model
ALLOWED_TYPES = {'C', 'H'}
#The valid strings for the "mfr" field in the cereal model
ALLOWED_MFR = {'Q','K','R','G','P','N','A'}
#List of the header names of the cereals model, id is included(Exist in DB only)
CEREAL_HEADERS_WITH_ID = ['id', 'name', 'mfr', 'type', 'calories', 'protein', 'fat', 'sodium', 
                          'fiber', 'carbo', 'sugars', 'potass', 'vitamins', 'shelf', 'weight', 'cups', 'rating']
#List of the header names for the cereals model, id not included(Used for uploading new cereals as ID is assigned from DB)
CEREAL_HEADERS_WITHOUT_ID = ['name', 'mfr', 'type', 'calories', 'protein', 'fat', 'sodium', 'fiber', 'carbo',
                             'sugars', 'potass', 'vitamins', 'shelf', 'weight', 'cups', 'rating']
#
FILTER_OPERATORS = {'eq' : '=', 'noteq' : '!=', 'less' : '<', 'greater' : '>', 'lesseq' : '<=', 'greatereq' : '>=' }

ALLOWED_VALUES = {'name' : None, 'mfr' : ALLOWED_MFR, 'type' : ALLOWED_TYPES, 'calories' : None, 'protein' : None, 'fat' : None,
                  'sodium' : None, 'fiber' : None,  'carbo' : None, 'sugars' : None, 'potass': None, 'vitamins' : None, 'shelf' : None,
                   'shelf' : None, 'weight' : None, 'cups' : None, 'rating': None, 'id': None}
