# About

This is a small collection of utilities used by Orbit Media's [Website Optimization](https://www.orbitmedia.com/website-optimization/) team. Contains independent scripts for varied SEO/CRO use cases. Use them however you like.

## Getting Started

Configure most scripts near the top of the file. That includes where to find files, a live URL to evaluate, what to name a CSV, etc.

Logfiles from nginx, Apache httpd, and other [common web servers are standardized](https://en.wikipedia.org/wiki/Common_Log_Format), but you may need to customize the regex somewhat near the top of each file for some. Use testparse.py for testing that.

# Scripts

## Testing

🐍 [testparse.py](https://github.com/Orbit-Media-Studios/wo-scripts/blob/main/testparse.py): Test the first 3 lines of a server log to confirm the regex format is correct

## Analysis 

### Logfiles 

🐍 [getcsv.py](https://github.com/Orbit-Media-Studios/wo-scripts/blob/main/getcsv.py): Converts a flat server log into CSV: a simple first test of your python environment!

🐍 [getexitpages.py](https://github.com/Orbit-Media-Studios/wo-scripts/blob/main/getexitpages.py): Discover and list all exit pages from a particular URL

🐍 [getpagectr.py](https://github.com/Orbit-Media-Studios/wo-scripts/blob/main/getpagectr.py): Summarize a folder of .gz-archived logs for counts and "CTRs" of page exit URLs

🐍 [getsitesearch.py](https://github.com/Orbit-Media-Studios/wo-scripts/blob/main/getsitesearch.py): Summarize site search data from a single access log in a CSV

🐍 [getsitesearchmulti.py](https://github.com/Orbit-Media-Studios/wo-scripts/blob/main/getsitesearchmulti.py): Summarize site search data from a folder full of .gz-archived logs

### International SEO

🐍 [getmixedlang.py](https://github.com/Orbit-Media-Studios/wo-scripts/blob/main/getmixedlang.py): Detect and isolate mixed language content using [lingua](https://github.com/pemistahl/lingua-py)


