#!/bin/bash

# Directory containing bird images
BIRDS_DIR="birds"

# API endpoint
API_URL="http://localhost:9001/detect"

# Check if the birds directory exists
if [ ! -d "$BIRDS_DIR" ]; then
    echo "Error: $BIRDS_DIR directory not found"
    exit 1
fi

# Loop through each file in the birds directory
for image in "$BIRDS_DIR"/*; do
    if [ -f "$image" ]; then
        echo "Processing: $image"
        
        # Send POST request to the API
        response=$(curl -s -X POST -F "image=@$image" "$API_URL")
        
        # Print the response
        echo "Response: $response"
        echo "------------------------"
    fi
done

echo "All images processed."