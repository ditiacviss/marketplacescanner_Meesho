

import datetime


# Function to log messages
def logger_info( message):
    # Get current time and format it
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Format the log message with timestamp
    log_entry = f"INFO::{current_time} - {message}\n"

    # Append log entry to the log file
    with open("logs/logs.txt", "a") as file:
        file.write(log_entry)
def logger_error( message):
    # Get current time and format it
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Format the log message with timestamp
    log_entry = f"ERROR::{current_time} - {message}\n"

    # Append log entry to the log file
    with open("logs/logs.txt", "a") as file:
        file.write(log_entry)

# Usage example

