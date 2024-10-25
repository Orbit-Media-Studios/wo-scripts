# Drilldown traffic summary for tier3 subfolders with support for .gz compressed logs

# Libraries
import re
import csv
import gzip
import os
from urllib.parse import urlparse
from collections import defaultdict

# Configuration
log_file_path = "nginx-logs/"  # Path to your log file (or folder of .gz files)
export_path = "tier3_folder_summary.csv"  # Updated: Path to the CSV export file for tier3 subfolders
process_folder = True  # Set to True if log_file_path is a folder of .gz files, False if it's a single plain text file
bot_list = ['bot','googlebot', 'bingbot', 'yandex', 'baiduspider', 'ahrefsbot', 'semrushbot', 'dataforseo','gptbot','pinterestbot','Cloudflare-Healthchecks','makemerrybot','applebot','statuscake','pingdom']  # List of bots to exclude
url_exceptions = ['_', 'contact', 'review', 'jsonapi', 'widget', 'blog', 'agreement', 'admincp', 'promokit','login','redirect','event-planner','dynamic','api','external','join']  # List of URL patterns to exclude

# Regular expression to parse log lines
log_pattern = re.compile(
    r'(?P<ip>[\d\.:a-fA-F]+)\s+-\s+-\s+\[(?P<timestamp>.+?)\]\s+(?P<status>\d+)\s+"(?P<method>\w+)\s+(?P<path>.+?)\s+HTTP/\d\.\d"\s+(?P<size>\d+)\s+".+?"\s+"(?P<user_agent>.*?)"'
)

# Function to parse a single log line
def parse_log_line(line):
    match = log_pattern.match(line)
    if match:
        return {
            'ip_address': match.group('ip'),
            'timestamp': match.group('timestamp'),
            'status_code': int(match.group('status')),
            'method': match.group('method'),
            'request_path': match.group('path'),
            'response_size': int(match.group('size')),
            'user_agent': match.group('user_agent'),
        }
    return None

# Function to extract level three folder from the request path (ignoring URL variables)
# Updated: Extracting the first three parts of the path to capture tier 3 subfolders
def extract_level_three_folder(request_path):
    parsed_url = urlparse(request_path)
    path = parsed_url.path  # Ignore the query string (i.e., no URL variables)
    
    # Remove leading/trailing slashes and split by "/"
    path_parts = path.strip("/").split("/")
    
    # Return the first three parts of the path as the "level three folder"
    if len(path_parts) >= 3:
        return "/" + path_parts[0] + "/" + path_parts[1] + "/" + path_parts[2]  # Ensure it starts with "/"
    return None

# Function to check if the user-agent is a bot based on the provided list
def is_bot(user_agent, bot_list):
    # Check if any bot string appears in the user-agent
    return any(bot in user_agent.lower() for bot in bot_list)

# Function to check if the URL contains any exclusion patterns
def is_excluded_url(request_path, url_exceptions):
    # Check if any of the patterns in the exclusion list are in the URL
    return any(exception in request_path for exception in url_exceptions)

# Function to process a single log file
def process_single_log_file(log_file_path, folder_hits, folder_pages, bot_list, url_exceptions):
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            process_log_line(line, folder_hits, folder_pages, bot_list, url_exceptions)

# Function to process a .gz compressed log file
def process_gz_log_file(log_file_path, folder_hits, folder_pages, bot_list, url_exceptions):
    with gzip.open(log_file_path, 'rt') as log_file:
        for line in log_file:
            process_log_line(line, folder_hits, folder_pages, bot_list, url_exceptions)

# Function to process log lines
def process_log_line(line, folder_hits, folder_pages, bot_list, url_exceptions):
    log_data = parse_log_line(line)
    
    if log_data and log_data['status_code'] == 200 and log_data['method'] == 'GET':
        # Skip if user-agent matches any bot in the list
        if is_bot(log_data['user_agent'], bot_list):
            return
        
        # Skip URLs that match any of the exclusion patterns
        if is_excluded_url(log_data['request_path'], url_exceptions):
            return
        
        folder = extract_level_three_folder(log_data['request_path'])  # Updated: Using the tier 3 folder extractor
        
        # Strip query parameters from the request path for unique subpage counting
        clean_path = urlparse(log_data['request_path']).path  # Ignore the query string
        
        if folder:
            folder_hits[folder] += 1  # Count the hit for this folder
            folder_pages[folder].add(clean_path)  # Track unique subpages, ignoring query params

# Function to process a folder of .gz compressed logs
def process_folder_of_gz_logs(folder_path, folder_hits, folder_pages, bot_list, url_exceptions):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.gz'):
            log_file_path = os.path.join(folder_path, file_name)
            print(f"Processing {log_file_path}...")
            process_gz_log_file(log_file_path, folder_hits, folder_pages, bot_list, url_exceptions)

# Function to export folder summary to a CSV file
def export_folder_summary_to_csv(folder_hits, folder_pages, export_path):
    with open(export_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['folder', 'total_subpages', 'total_hits'])  # Write header
        
        for folder, hits in folder_hits.items():
            total_subpages = len(folder_pages[folder])  # Count unique subpages
            csv_writer.writerow([folder, total_subpages, hits])  # Write folder data

# Function to process the log file or folder of logs and export folder summary to CSV
def process_folder_summary(log_file_path, export_path, process_folder, bot_list, url_exceptions):
    folder_hits = defaultdict(int)  # Track total hits per folder
    folder_pages = defaultdict(set)  # Track unique subpages per folder
    
    if process_folder:
        # Process a folder of .gz logs
        process_folder_of_gz_logs(log_file_path, folder_hits, folder_pages, bot_list, url_exceptions)
    else:
        # Process a single log file
        process_single_log_file(log_file_path, folder_hits, folder_pages, bot_list, url_exceptions)
    
    # Export results to CSV
    export_folder_summary_to_csv(folder_hits, folder_pages, export_path)

# Process the log file or folder and export the folder summary to CSV
process_folder_summary(log_file_path, export_path, process_folder, bot_list, url_exceptions)

print(f"Processing complete! Tier 3 folder summary saved to {export_path}")
