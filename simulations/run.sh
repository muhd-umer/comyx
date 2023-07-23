#!/bin/bash

echo -e "\033[34mRunning all settings as defined in config...\n\033[0m"

# Determine the current directory
current_dir=$(basename $(pwd))

# Import the setting dictionary based on the current directory
if [ "$current_dir" == "simulations" ]; then
    from="from config import setting"
elif [ "$current_dir" == "comm-fyp" ]; then
    from="from simulations.config import setting"
else
    echo "Please execute this script from either simcomm/ or simulations/ folder."
    exit 1
fi

# Get all the keys in the setting dictionary
keys=$(python -c "$from; print('\n'.join(setting.keys()))")

# Iterate over the keys and run main.py with the key as an argument
for key in $keys
do
    if [ "$current_dir" == "simulations" ]; then
        python main.py -S $key
    elif [ "$current_dir" == "comm-fyp" ]; then
        python simulations/main.py -S $key
    fi
done