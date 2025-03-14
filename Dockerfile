# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy all files
COPY . .
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Install dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app/resource_scheduler.py"]
