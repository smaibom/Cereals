FROM mcr.microsoft.com/mssql/server:2019-latest

# Create work directory
RUN mkdir -p /usr/work
WORKDIR /usr/work

# Copy all scripts into working directory
COPY scripts /usr/work/

# Grant permissions for the import-data script to be executable
USER root
RUN chmod +x /usr/work/import-data.sh
RUN chmod +x /usr/work/entrypoint.sh
USER mssql
EXPOSE 1433

CMD /bin/bash /usr/work/entrypoint.sh
