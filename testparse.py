# Just prints the first three lines of the log file to test regex format - tests OK!
import re
from datetime import datetime

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

# Function to print the first three log entries
def print_first_three_logs(log_file_path):
    count = 0
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            log_data = parse_log_line(line)
            if log_data:
                print(log_data)
                count += 1
            if count >= 3:
                break

# Specify your log file path
log_file_path = "nginx-logs/access.log"

# Print the first three log entries
print_first_three_logs(log_file_path)