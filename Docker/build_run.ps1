docker build -t mssqlserver -f Dockerfile .
docker run -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=Password1!' -e 'MSSQL_PID=Express' --name sqlserver -p 1433:1433 -d -v mssqlvol:/var/ms_sql mssqlserver
