# Script to analyze a single nginx log file to summarize exit page behavior. Stores the next page visited as "next_url" as a click-through rate estimate.
# This script is a simplified intermediary step towards getpagectr.py

# Libraries
import re
import csv
from datetime import datetime

# Configuration
log_file_path = "nginx-logs/access.log"  # Path to your log file
export_path = "analysis.csv"             # Path to the CSV export file
filter_path = "/"                        # Path you want to filter by, e.g., homepage "/"

# Adjusted regular expression to parse log lines
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
def export_filtered_logs_with_next_url(log_file_path, export_path, filter_path):
    # Dictionary to store log entries by IP for tracking the next URL
    log_by_ip = {}

    # Open the log file and CSV output file
    with open(log_file_path, 'r') as log_file, open(export_path, 'w', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=['ip_address', 'timestamp', 'status_code', 'method', 'request_path', 'response_size', 'user_agent', 'next_url'])
        csv_writer.writeheader()

        # Read each line from the log file
        for line in log_file:
            log_data = parse_log_line(line)
            
            # Only process logs with status code 200 and full page requests
            if log_data and log_data['status_code'] == 200 and log_data['method'] == 'GET':
                ip = log_data['ip_address']
                
                # Check if we have previously encountered this IP visiting the homepage (filter_path)
                if ip in log_by_ip and log_by_ip[ip]['next_url'] is None:
                    # If the next URL for the previous homepage visit is not set, assign the current request path
                    log_by_ip[ip]['next_url'] = log_data['request_path']
                    
                    # Write the previous homepage log to the CSV (now with the next_url set)
                    csv_writer.writerow(log_by_ip[ip])
                    
                    # Remove the entry from the dictionary, as we've finished processing it
                    del log_by_ip[ip]

                # If the current log entry is for the homepage, store it for later processing
                if log_data['request_path'] == filter_path:
                    log_by_ip[ip] = {
                        'ip_address': log_data['ip_address'],
                        'timestamp': log_data['timestamp'],
                        'status_code': log_data['status_code'],
                        'method': log_data['method'],
                        'request_path': log_data['request_path'],
                        'response_size': log_data['response_size'],
                        'user_agent': log_data['user_agent'],
                        'next_url': None  # Initialize with None
                    }

# Process the log file and export filtered records to CSV
export_filtered_logs_with_next_url(log_file_path, export_path, filter_path)

print(f"Export complete! Filtered logs saved to {export_path}")
