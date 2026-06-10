# Use a lightweight official Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python script
COPY main.py .

# print() statements show up instantly in truenas logs
ENV PYTHONUNBUFFERED=1 

# Run the script
CMD ["python", "main.py"]
