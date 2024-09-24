# Use the official Python image as the base
FROM python:3.9-slim


# Update the package list and install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


# Set the working directory in the container
WORKDIR /app

# Copy requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app's code to the container
COPY ./data/ /data/
COPY ./frontend/ /frontend/

WORKDIR /frontend

# Expose the port that Streamlit runs on
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "index.py", "--server.port=8501", "--server.address=0.0.0.0"]
