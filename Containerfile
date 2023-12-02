# Use a smaller base image
FROM python:3.9-slim AS build

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /code

# Copy requirements.txt and install dependencies
RUN apt-get update && apt-get install -y curl
COPY curl_math_pages.sh .
COPY urls.txt .
RUN mkdir data
RUN "./curl_math_pages.sh"

# Copy the rest of the code
COPY . .

EXPOSE 8000

#CMD ["tail", "-f", "/dev/null"]
CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]