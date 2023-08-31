FROM python:3.10-slim

# Setup directories
RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app

# Install necessary Python packages
COPY requirements.txt /opt/dagster/app/
RUN pip install --no-cache-dir -r /opt/dagster/app/requirements.txt

# Copy necessary files to the image
COPY src/etl_flow/etl.py src/etl_flow/workspace.yaml src/etl_flow/sql_queries.py /opt/dagster/app/
COPY src/etl_flow/dagster.yaml /opt/dagster/dagster_home/

# Setup environment variable
ENV DAGSTER_HOME=/opt/dagster/dagster_home/

# Set working directory
WORKDIR /opt/dagster/app

# Expose port
EXPOSE 3000

# Entry point for the Dagster webserver
ENTRYPOINT ["dagit", "-w", "workspace.yaml", "-h", "0.0.0.0", "-p", "3000"]
