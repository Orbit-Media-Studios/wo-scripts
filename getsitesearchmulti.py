# Script to analyze a folder of .gz nginx log files to extract site search terms and their counts

# Libraries
import re
import csv
import gzip
import os
from urllib.parse import parse_qs, urlparse
from datetime import datetime

# Configuration
log_folder = "nginx-logs-testing/"  # Path to folder containing .gz log files
export_path = "search_terms_analysis.csv"  # Path to the CSV export file
search_url_path = "/search"  # Path for search requests
search_param = "q"  # Query parameter for search term

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

# Function to extract search terms from the request path
def extract_search_term(request_path, search_url_path, search_param):
    parsed_url = urlparse(request_path)
    if parsed_url.path.startswith(search_url_path):
        query_params = parse_qs(parsed_url.query)
        if search_param in query_params:
            return query_params[search_param][0]  # Return the first value for the search parameter
    return None

# Function to process logs from a .gz file and collect search terms
def process_search_terms_from_gz(gz_file, search_url_path, search_param, search_terms):
    with gzip.open(gz_file, 'rt') as f:  # 'rt' mode reads the file as text
        for line in f:
            log_data = parse_log_line(line)
            
            if log_data and log_data['status_code'] == 200 and log_data['method'] == 'GET':
                search_term = extract_search_term(log_data['request_path'], search_url_path, search_param)
                if search_term:
                    if search_term in search_terms:
                        search_terms[search_term] += 1
                    else:
                        search_terms[search_term] = 1

# Function to process all .gz log files in a folder
def process_search_terms_from_folder(folder, search_url_path, search_param):
    search_terms = {}  # Dictionary to store search term counts

    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        
        if file_name.endswith('.gz'):
            print(f"Processing .gz file: {file_name}")
            process_search_terms_from_gz(file_path, search_url_path, search_param, search_terms)
        else:
            print(f"Skipping non-.gz file: {file_name}")

    return search_terms

# Function to export search terms and counts to a CSV file
def export_search_terms_to_csv(search_terms, export_path):
    sorted_terms = sorted(search_terms.items(), key=lambda x: x[1], reverse=True)  # Sort by count, descending

    with open(export_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['search_term', 'count'])  # Write header
        csv_writer.writerows(sorted_terms)  # Write search terms and counts

# Process all logs in the folder and export search terms to CSV
search_terms = process_search_terms_from_folder(log_folder, search_url_path, search_param)
export_search_terms_to_csv(search_terms, export_path)

print(f"Processing complete! Search terms saved to {export_path}")
