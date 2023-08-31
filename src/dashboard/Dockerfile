# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary Python packages
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy Streamlit script and pages folder into the container
COPY src/dashboard/Dashboard.py /app/
COPY src/dashboard/pages /app/pages
COPY src/dashboard/imgs /app/imgs

# Run streamlit_app.py when the container launches
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "Dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
