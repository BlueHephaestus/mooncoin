#!/bin/bash

# Go to your project directory (where the repo is located)
MOON_DIR=/home/blue/Projects/mooncoin

cd $MOON_DIR

# Update the files
python3.11 main.py

# Stage the files
git add moon.png
git add metadata.json

# Commit the file with a message
today=$(date +"%Y-%m-%d")
git commit -m "Auto update $today"

# Push to the GitHub repository
git push origin main
