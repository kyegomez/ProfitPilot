# Use an official Python runtime as the parent image
FROM python:3.8-slim

# Set the working directory in the docker image
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required tools and dependencies
RUN apt-get update && apt-get install -y && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install clarifai-grpc & \
    pip install streamlit & \
    pip install streamlit-chat & \
    pip install pydantic & \
    pip install langchain & \
    pip install openai & \
    pip install transformers & \
    pip install faiss-gpu==1.7.2 & \
    pip install langchain-experimental & \
    pip install clarifai & \
    pip install torch & \
    pip install pandas

# Expose the port the app runs on
EXPOSE 80

# Command to run the application
CMD ["python3", "example.py"]



