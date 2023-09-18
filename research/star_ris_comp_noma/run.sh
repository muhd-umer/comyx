#!/bin/bash

echo -e "\033[34mRunning all settings as defined in config...\n\033[0m"

# Determine the current directory
current_dir=$(basename $(pwd))

# Import the setting dictionary based on the current directory
from="from config import setting"

# Get all the keys in the setting dictionary
keys=$(python -c "$from; print('\n'.join(setting.keys()))")

# Iterate over the keys and run main.py with the key as an argument
for key in $keys
do
    python main.py --setting $key
done