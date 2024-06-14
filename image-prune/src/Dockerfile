# Stage 1: Build stage
FROM python:3.9-slim AS builder

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies for Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt ./

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install grpcio-tools for generating Python files from protobuf definitions
RUN pip install --no-cache-dir grpcio-tools

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Generate the Python files from the protobuf definition
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. containerd_services.proto


# Stage 2: Runtime stage
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy only the necessary files from the previous stage
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /usr/src/app .

# Ensure the virtual environment is activated
ENV PATH="/opt/venv/bin:$PATH"

# Run the script
CMD ["python", "./main.py"]
