# Drilldown traffic/subfolder summary for all tier1 folders

# Libraries
import re
import csv
from urllib.parse import urlparse
from collections import defaultdict

# Configuration
log_file_path = "nginx-logs/access.log"  # Path to your log file
export_path = "folder_summary.csv"  # Path to the CSV export file
bot_list = ['bot','googlebot', 'bingbot', 'yandex', 'baiduspider', 'ahrefsbot', 'semrushbot', 'dataforseo','gptbot','pinterestbot','Cloudflare-Healthchecks','makemerrybot','applebot','statuscake','pingdom']  # List of bots to exclude
url_exceptions = ['_', 'contact', 'review', 'jsonapi', 'widget', 'blog', 'agreement','admincp','promokit']  # List of URL patterns to exclude

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

# Function to extract level one folder from the request path (ignoring URL variables)
def extract_level_one_folder(request_path):
    parsed_url = urlparse(request_path)
    path = parsed_url.path  # Ignore the query string (i.e., no URL variables)
    
    # Remove leading/trailing slashes and split by "/"
    path_parts = path.strip("/").split("/")
    
    # Return the first part of the path as the "level one folder"
    if path_parts:
        return "/" + path_parts[0]  # Ensure it starts with a "/"
    return None

# Function to check if the user-agent is a bot based on the provided list
def is_bot(user_agent, bot_list):
    # Check if any bot string appears in the user-agent
    return any(bot in user_agent.lower() for bot in bot_list)

# Function to check if the URL contains any exclusion patterns
def is_excluded_url(request_path, url_exceptions):
    # Check if any of the patterns in the exclusion list are in the URL
    return any(exception in request_path for exception in url_exceptions)

# Function to process the log file and collect folder summaries, ignoring bots and URL variables
def process_folder_summary(log_file_path, bot_list):
    folder_hits = defaultdict(int)  # Track total hits per folder
    folder_pages = defaultdict(set)  # Track unique subpages per folder

    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            log_data = parse_log_line(line)
            
            if log_data and log_data['status_code'] == 200 and log_data['method'] == 'GET':
                # Skip if user-agent matches any bot in the list
                if is_bot(log_data['user_agent'], bot_list):
                    continue
                
                # Skip URLs that match any of the exclusion patterns
                if is_excluded_url(log_data['request_path'], url_exceptions):
                    continue

                folder = extract_level_one_folder(log_data['request_path'])
                
                # Strip query parameters from the request path for unique subpage counting
                clean_path = urlparse(log_data['request_path']).path  # Ignore the query string
                
                if folder:
                    folder_hits[folder] += 1  # Count the hit for this folder
                    folder_pages[folder].add(clean_path)  # Track unique subpages, ignoring query params

    return folder_hits, folder_pages

# Function to export folder summary to a CSV file
def export_folder_summary_to_csv(folder_hits, folder_pages, export_path):
    with open(export_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['folder', 'total_subpages', 'total_hits'])  # Write header
        
        for folder, hits in folder_hits.items():
            total_subpages = len(folder_pages[folder])  # Count unique subpages
            csv_writer.writerow([folder, total_subpages, hits])  # Write folder data


# Process the log file and export folder summary to CSV, ignoring bots
folder_hits, folder_pages = process_folder_summary(log_file_path, bot_list)
export_folder_summary_to_csv(folder_hits, folder_pages, export_path)


print(f"Processing complete! Folder summary saved to {export_path}")
