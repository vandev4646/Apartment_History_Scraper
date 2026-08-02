# Use a slim, lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first to leverage Docker's caching mechanism
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the scraper code
COPY . .

# Run the scraper script when the container starts
CMD ["python", "webscraper_main.py"]
