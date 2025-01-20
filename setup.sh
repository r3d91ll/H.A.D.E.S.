#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    case $color in
        "green") echo -e "\033[0;32m$message\033[0m" ;;
        "red") echo -e "\033[0;31m$message\033[0m" ;;
        "yellow") echo -e "\033[1;33m$message\033[0m" ;;
    esac
}

# Check for required commands
print_status "yellow" "Checking prerequisites..."

if ! command_exists docker; then
    print_status "red" "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command_exists docker compose; then
    print_status "red" "Error: Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

if ! command_exists npm; then
    print_status "red" "Error: npm is not installed. Please install Node.js and npm first."
    exit 1
fi

# Setup environment variables
if [ ! -f .env ]; then
    if [ -f env.example ]; then
        print_status "yellow" "Creating .env file from env.example..."
        cp env.example .env
        print_status "yellow" "Please edit .env file with your desired settings"
    else
        print_status "red" "Error: Neither .env nor env.example file found"
        exit 1
    fi
fi

# Load environment variables
set -a
source .env
set +a

# Build and start ArangoDB container
print_status "yellow" "Building and starting ArangoDB container..."
docker compose down 2>/dev/null
docker compose up -d

# Wait for ArangoDB to be ready
print_status "yellow" "Waiting for ArangoDB to be ready..."
max_attempts=30
attempt=1
while [ $attempt -le $max_attempts ]; do
    if curl -s -u "${ARANGO_USERNAME}:${ARANGO_PASSWORD}" "${ARANGO_URL}/_api/version" >/dev/null; then
        print_status "green" "ArangoDB is ready!"
        break
    fi
    print_status "yellow" "Attempt $attempt/$max_attempts: ArangoDB is not ready yet. Waiting..."
    sleep 2
    attempt=$((attempt + 1))
done

if [ $attempt -gt $max_attempts ]; then
    print_status "red" "Error: ArangoDB failed to start within the expected time."
    exit 1
fi

# Create database if it doesn't exist
print_status "yellow" "Creating/verifying database..."
curl -s -u "${ARANGO_USERNAME}:${ARANGO_PASSWORD}" "${ARANGO_URL}/_api/database" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"${ARANGO_DATABASE}\"}" > /dev/null

# Install npm dependencies
print_status "yellow" "Installing npm dependencies..."
npm install

# Build TypeScript project
print_status "yellow" "Building TypeScript project..."
npm run build

print_status "green" "Setup completed successfully!"
print_status "yellow" "You can now start using HADES with your IDE."
