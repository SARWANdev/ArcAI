#!/bin/bash

# Step 1: Go to the directory
cd /home/pse04/arcai/backend/arcai/ || { echo "Failed to cd"; exit 1; }

# Step 2: Create virtual environment with python3.11
python3.11 -m venv venv

# Step 3: Activate the virtual environment
source venv/bin/activate

# Step 4: Install requirements
pip install -r requirements.txt

# Step 5: Run the Python script with the specified PYTHONPATH and python interpreter
PYTHONPATH=/home/pse04/arcai/backend/arcai/ /home/pse04/arcai/backend/arcai/venv/bin/python /home/pse04/arcai/backend/arcai/controller/__init__.py
