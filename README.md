# Web Log Stats
Python script to parse through a web log file and return the number of requests and unique IPs in a given time period

It takes web (apache or nginx for now) log files via -f, the number of hours back you'd like to look -t (Default = 24 hours), and if you want the actual list of unique IPs -i or a list of the Top N most common IPs via -n

Options:
```
-h, --help  show this help message and exit
-i, --ips   shows list of unique IPs
-t HOURS    number of hours back you want to look
-n IPS      List the n most common IPs to visit in the given time period
-f FILES, --files=FILES
       		list of apache log file paths
```

Usage Examples:
```
python apacheCounter.py -f "httpd-access.log"
python apacheCounter.py -i -t 48 -n 10 -f "../path/to/httpd-access.log.0, ../path/to/httpd-access.log.1"
