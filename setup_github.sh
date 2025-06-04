#!/bin/bash
# Setup script to initialize git repository and push to GitHub

echo "Setting up Git repository for SCD40 sensor project..."

# Configure git with your credentials
git config --global user.name "jfarley-ux"
git config --global user.email "jamie.farley@hotmail.co.uk"

# Initialize git repository
git init

# Add files
git add scd40_sensor.py requirements.txt README.md

# Initial commit
git commit -m "Initial commit: SCD40 CO2 sensor script for Raspberry Pi"

# Add remote repository
git remote add origin https://github.com/jfarley-ux/sensor.git

# Create main branch and push
git branch -M main
git push -u origin main

echo "Repository setup complete!"
