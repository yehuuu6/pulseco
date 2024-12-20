import os
from typing import List
from logging import getLogger, Logger, basicConfig, INFO

"""
Provides logging functionality for the pulseco app.
"""

# If logs directory does not exist, create it
try:
    os.makedirs("app/logs", exist_ok=True)
except Exception as e:
    print(f"Failed to create logs directory: {e}")
    exit(1)
# List of log files
log_files: List[str] = ["chat.log", "commands.log", "server.log"]

# Create log files if they don't exist
for log_file in log_files:
    if not os.path.exists(f"app/logs/{log_file}"):
        print(f"Creating {log_file}...")
        with open(f"app/logs/{log_file}", "w") as f:
            f.write("")
        print(f"{log_file} created.")


# Create the main logger
main_logger: Logger = getLogger("pulseco")  # Create the main logger
basicConfig(
    filename="app/logs/server.log",
    level=INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
