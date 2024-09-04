#!/usr/bin/env bash
# Use this script to export all variables from .env file
# $ . export_env.sh /path/to/.env

VERBOSE=false
ENV_FILE='.env'

# Iterate over all arguments to check for -v and file path
for arg in "$@"; do
    if [[ "$arg" == "-v" ]]; then
        VERBOSE=true
    elif [[ "$arg" != "-"* ]]; then
        ENV_FILE="$arg"
    fi
done

if [[ -f "$ENV_FILE" ]]; then
    while IFS= read -r line; do
        # Skip empty lines and comments
        if [[ -n "$line" && "$line" != \#* ]]; then
            # Export each variable while trimming spaces around the '='
            var_name=$(echo "$line" | cut -d '=' -f 1 | xargs)
            var_value=$(echo "$line" | cut -d '=' -f 2- | xargs)
            if [[ "$VERBOSE" == true ]]; then
                echo "Exporting $var_name=$var_value"
            fi
            export "$var_name=$var_value"
        fi
    done < "$ENV_FILE"
    echo "Environment variables loaded from '$ENV_FILE'."
else
    echo "Error: '$ENV_FILE' does not exist."
fi
