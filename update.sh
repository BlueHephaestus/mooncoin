#!/bin/bash

# Go to your project directory (where the repo is located)
MOON_DIR=/home/blue/Projects/mooncoin

cd $MOON_DIR

# Update the file
python3.11 main.py

# Stage the file
git add moon.png

# Commit the file with a message
today=$(date + "%Y-%m-%d")
git commit -m "Auto update $today"

# Push to the GitHub repository
git push origin main
