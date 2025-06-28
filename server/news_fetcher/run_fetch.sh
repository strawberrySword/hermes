#!/bin/bash

# Activate virtual environment
source /Users/avivboa/workspace/recommendation/news_fetcher/venv/bin/activate

# Run the scheduler script (which calls run_fetcher from fetch_pipeline.py)
python /Users/avivboa/workspace/recommendation/news_fetcher/scheduler.py
