# wait for the SQL Server to come up
sleep 45s

#run the setup script to create the DB and the schema in the DB
/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "Password1!" -i setup.sql

# import the data from the csv file
#/opt/mssql-tools/bin/bcp cereals.dbo.cereal in "/usr/work/cereals.csv" -c -t',' -S localhost -U SA -P "Password1!"
