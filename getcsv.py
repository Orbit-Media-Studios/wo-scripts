# Script to analyze nginx logs to summarize homepage exit behavior
#
# 1. Loop through rotated logfile archives in ascending chronological order
# 2. Parse to something clean using regex (array, sql, whatever)
# 3. Record only rows that access the homepage, leaving a blank column for “page_exit_url”
# 4. Eval every subsequent row: IF ip_address IN (step #2 dataset) AND page_exit_url NOT BLANK THEN UPDATE page_exit_url

# Libraries
import re
import csv
from datetime import datetime

# Configuration
log_file_path = "nginx-logs/access.log"  # Path to your log file
export_path = "analysis.csv"             # Path to the CSV export file

# Regular expression to parse log lines
log_pattern = re.compile(
    r'(?P<ip>[\d\.:a-fA-F]+)\s+-\s+-\s+\[(?P<timestamp>.+?)\]\s+(?P<status>\d+)\s+"(?P<method>\w+)\s+(?P<path>.+?)\s+HTTP/\d\.\d"\s+(?P<size>\d+)\s+".+?"\s+"(?P<user_agent>.*?)"'
)

# Function to parse a single log line
def parse_log_line(line):
    match = log_pattern.match(line)
    if match:
        # Parse timestamp
        timestamp_str = match.group('timestamp')
        timestamp = datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S %z")
        
        return {
            'ip_address': match.group('ip'),
            'timestamp': timestamp,
            'status_code': int(match.group('status')),
            'method': match.group('method'),
            'request_path': match.group('path'),
            'response_size': int(match.group('size')),
            'user_agent': match.group('user_agent'),
        }
    return None

# Function to process the log file and export matching records to CSV
def export_filtered_logs(log_file_path, export_path):
    with open(log_file_path, 'r') as log_file, open(export_path, 'w', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=['ip_address', 'timestamp', 'status_code', 'method', 'request_path', 'response_size', 'user_agent'])
        csv_writer.writeheader()
        
        for line in log_file:
            log_data = parse_log_line(line)
            if log_data:  # Check if log_data is not None
                csv_writer.writerow(log_data)

# Process the log file and export filtered records to CSV
export_filtered_logs(log_file_path, export_path)

print(f"Export complete! Filtered logs saved to {export_path}")
