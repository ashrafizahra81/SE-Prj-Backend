# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . .

# Expose the port on which your DRF app runs (e.g., 8000)
EXPOSE 8000

# Define the command to start your DRF app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
