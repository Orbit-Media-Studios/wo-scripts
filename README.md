# About

Small library of SEO utilities used by Orbit Media Studios optimization team. Contains various independent utilities.

Most scripts save to a CSV in the location that you configure at the top of the file. Some scripts have additional configurations that you can set, too. 

Logfiles from nginx, apache/httpd, and other common web servers are fairly standardized, but you may need to customize the regex somewhat near the top of each file for some. Use testparse.py for testing that.

# Scripts

## Testing

🐍 testparse.py: Tests the first 3 lines of a server log to confirm the regex format is correct

## Analysis 

🐍 getcsv.py: Just converts a flat logfile into CSV format. Good starting point to test for save permissions.
🐍 getmixedlang.py: Detect mixed language content using lingua (used to clean up language signals for international SEO)
🐍 getpagectr.py: Summarizes a folder of .gz archived logfiles for "CTRs" to each next URL (builds on getpagenext.py's approach)
🐍 getpagenext.py: Gets all log items for a filtered URL, including the next URL that each IP accessed. 
🐍 getsitesearch.py: Summarizes site search data where a URL parameter was used.