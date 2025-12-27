#!/bin/bash

# Define environment name
ENV_NAME="rag_vcf_env"

echo "Creating clean Conda environment: $ENV_NAME..."

# Create conda environment with Python 3.10
conda create -n $ENV_NAME python=3.10 -y

# Instructions for the user
echo ""
echo "----------------------------------------------------------------"
echo "Environment created successfully!"
echo "----------------------------------------------------------------"
echo "To activate the environment and install dependencies, run:"
echo ""
echo "    conda activate $ENV_NAME"
echo "    pip install -r requirements.txt"
echo "    streamlit run app.py"
echo ""
echo "----------------------------------------------------------------"
