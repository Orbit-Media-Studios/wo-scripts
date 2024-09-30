# About

Small library of SEO utilities used by Orbit Media Studio's [Website Optimization](https://www.orbitmedia.com/website-optimization/) team. Contains various independent utilities.

Most scripts can be configured near the top of the file. That usually includes a place to save a CSV file and where to find other files.

Logfiles from nginx, apache/httpd, and other [common web servers are standardized](https://en.wikipedia.org/wiki/Common_Log_Format), but you may need to customize the regex somewhat near the top of each file for some. Use testparse.py for testing that.

# Scripts

## Testing

🐍 [testparse.py](https://github.com/Orbit-Media-Studios/wo-scripts/blob/main/testparse.py): Tests the first 3 lines of a server log to confirm the regex format is correct

## Analysis 

🐍 [getcsv.py](https://github.com/Orbit-Media-Studios/wo-scripts/blob/main/getcsv.py): Just converts a flat logfile into CSV format, simple first test of your python environment

🐍 [getexitpages.py](https://github.com/Orbit-Media-Studios/wo-scripts/blob/main/getexitpages.py): Loop through a single server log to pair up exit pages from a particular URL, export CSV

🐍 [getmixedlang.py](https://github.com/Orbit-Media-Studios/wo-scripts/blob/main/getmixedlang.py): Detect mixed language content with lingua, tidy language signals for international SEO

🐍 [getpagectr.py](https://github.com/Orbit-Media-Studios/wo-scripts/blob/main/getpagectr.py): Summarizes a folder of .gz-archived logfiles for "CTRs" to each discovered exit URL

🐍 [getsitesearch.py](https://github.com/Orbit-Media-Studios/wo-scripts/blob/main/getsitesearch.py): Summarizes site search data from a single access log in a CSV

🐍 [getsitesearchmulti.py](https://github.com/Orbit-Media-Studios/wo-scripts/blob/main/getsitesearchmulti.py): Same as above, but processes a folder full of .gz-archived logs

