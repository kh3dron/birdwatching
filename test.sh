#!/bin/bash


# API_URL="http://localhost:9001/detect" # works
# API_URL="http://127.0.0.1:9001/detect" # works
API_URL="http://100.72.208.26:9111/detect" # fails

# Get image from API
curl -X GET $API_URL