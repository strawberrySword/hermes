#!/bin/bash

# Absolute path to Python
PYTHON_PATH=$(which python3)

# Absolute path to fetch pipeline
SCRIPT_PATH="$(pwd)/fetch_pipeline.py"

# Log file location
LOG_PATH="$(pwd)/fetch.log"

# Cron schedule (every 2 hours)
CRON_JOB="0 */2 * * * $PYTHON_PATH $SCRIPT_PATH >> $LOG_PATH 2>&1"

# Add to crontab if not already present
(crontab -l 2>/dev/null | grep -v -F "$SCRIPT_PATH" ; echo "$CRON_JOB") | crontab -

echo "Cron job installed to run every 2 hours."

