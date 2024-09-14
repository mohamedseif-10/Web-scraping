import re
from datetime import datetime, timedelta

# Function to parse the time string and return the date
# This is the very small example of how we can clean the data

def parse_time_string(time_str):
    current_time = datetime.now()
    result_time = current_time

    # Check for time units and extract the number
    if "hour" in time_str:
        match = re.search(r"\d+", time_str)
        if match:
            hours = int(match.group())
            result_time = current_time - timedelta(hours=hours)
    elif "day" in time_str:
        match = re.search(r"\d+", time_str)
        if match:
            days = int(match.group())
            result_time = current_time - timedelta(days=days)
    elif "year" in time_str:
        match = re.search(r"\d+", time_str)
        if match:
            years = int(match.group())
            result_time = current_time - timedelta(days=365 * years)
    elif "today" in time_str:
        result_time = current_time

    return result_time.strftime("%Y-%m-%d")
