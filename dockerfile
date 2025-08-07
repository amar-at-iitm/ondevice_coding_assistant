# Use a slim, official Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the generated script (this will be done by the Python script)
COPY main.py .

# The command to run the script
CMD ["python", "main.py"]