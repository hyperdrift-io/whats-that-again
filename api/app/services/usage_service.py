"""
Usage tracking service for the WhatsThatAgain API
"""

import os
from datetime import datetime
from typing import Tuple

# Constants
MAX_DAILY_QUERIES = 100
USAGE_FILE = "usage_count.txt"


def check_usage_limit() -> Tuple[bool, str]:
    """
    Check if the daily usage limit has been reached
    Returns: (is_limit_reached, usage_info)
    """
    today = datetime.now().strftime("%Y-%m-%d")
    count = 0
    last_date = None

    # Create the file if it doesn't exist
    if not os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "w") as f:
            f.write(f"{today}:0")

    # Read the current usage
    with open(USAGE_FILE, "r") as f:
        content = f.read().strip()
        if content:
            parts = content.split(":")
            if len(parts) == 2:
                last_date, count_str = parts
                try:
                    count = int(count_str)
                except ValueError:
                    count = 0

    # Reset count if it's a new day
    if last_date != today:
        count = 0
        last_date = today

    # Check if limit is reached
    is_limit_reached = count >= MAX_DAILY_QUERIES

    # Update the usage file
    if not is_limit_reached:
        count += 1
        with open(USAGE_FILE, "w") as f:
            f.write(f"{today}:{count}")

    # Prepare usage info
    usage_info = f"Queries today: {count}/{MAX_DAILY_QUERIES}"

    return is_limit_reached, usage_info
