import urllib
secret = 'secret-key-goes-here'
dbstring = 'DRIVER={SQL Server};SERVER=localhost;PORT=1433;DATABASE=cereals;UID=sa;PWD=Password1!'
params = urllib.parse.quote_plus(dbstring)
db_uri = "mssql+pyodbc:///?odbc_connect=%s" % params