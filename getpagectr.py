# Script to analyze a folder of gzipped nginx log files to summarize page exit behavior
# Stores the next page visited as "next_url" as an imperfect click-through rate estimate
# Then summarizes "CTR" statistics from a particular page in a CSV

# Libraries
import gzip
import os
import re
import pandas as pd
from datetime import datetime

# Configuration
log_folder = "nginx-logs/"             # Path to folder with logs
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

# Function to process logs from a .gz file
def process_logs_from_gz(gz_file, filter_path, log_by_ip):
    with gzip.open(gz_file, 'rt') as f:  # 'rt' mode reads the file as text
        for line in f:
            log_data = parse_log_line(line)
            if log_data and log_data['status_code'] == 200:
                ip = log_data['ip_address']
                
                # If the current log entry is for the filter_path, store it
                if log_data['request_path'] == filter_path:
                    log_by_ip[ip] = {
                        'timestamp': log_data['timestamp'],
                        'next_url': None  # Initialize with None
                    }
                # If this is a subsequent request from the same IP, mark it as the next URL
                elif ip in log_by_ip and log_by_ip[ip]['next_url'] is None:
                    log_by_ip[ip]['next_url'] = log_data['request_path']

# Function to process logs from a folder
def process_logs_from_folder(folder, filter_path):
    log_by_ip = {}
    all_log_entries = []

    # Read each file in the folder
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        
        if file_name.endswith('.gz'):
            print(f"Processing .gz file: {file_name}")
            process_logs_from_gz(file_path, filter_path, log_by_ip)
        else:
            print(f"Skipping non-.gz file: {file_name}")

    # Convert log_by_ip dictionary to a list of log entries (filtering out None next_urls)
    for ip, entry in log_by_ip.items():
        if entry['next_url']:
            all_log_entries.append({
                'ip_address': ip,
                'next_url': entry['next_url'],
                'timestamp': entry['timestamp']
            })

    return pd.DataFrame(all_log_entries)

# Function to generate summary
def generate_summary(df):
    # 1. Calculate total hits
    total_hits = len(df)

    # 2. Calculate unique next_url counts
    next_url_counts = df['next_url'].value_counts().reset_index()
    next_url_counts.columns = ['next_url', 'count']

    # 3. Add percentage of total hits
    next_url_counts['percent_of_total'] = (next_url_counts['count'] / total_hits) * 100

    # 4. Calculate date range
    min_timestamp = df['timestamp'].min()
    max_timestamp = df['timestamp'].max()

    # Display meta metrics
    print(f"Total Hits: {total_hits}")
    print(f"Date Range: {min_timestamp} to {max_timestamp}")

    return next_url_counts, total_hits, min_timestamp, max_timestamp

# Function to write data to CSV, including meta metrics at the top
def write_to_csv(next_url_summary, total_hits, min_timestamp, max_timestamp, export_path):
    # Create a dataframe for meta information
    meta_info = pd.DataFrame({
        'Metric': ['Total Hits', 'Date Range'],
        'Value': [total_hits, f"{min_timestamp} to {max_timestamp}"]
    })

    # Write meta information and summary to CSV
    with open(export_path, 'w') as f:
        # Write meta information to columns D and E
        meta_info.to_csv(f, header=False, index=False)

        # Write an empty row after meta information
        f.write('\n')

        # Append the next_url summary
        next_url_summary.to_csv(f, index=False)

# Process the log files
df = process_logs_from_folder(log_folder, filter_path)

# Generate summary
next_url_summary, total_hits, min_timestamp, max_timestamp = generate_summary(df)

# Save summary and meta metrics to CSV
write_to_csv(next_url_summary, total_hits, min_timestamp, max_timestamp, export_path)

print(f"Processing complete. Summary saved to {export_path}")
