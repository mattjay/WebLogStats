# apacheCounter.py
Python script to parse through an Apache log file and return the number of requests and unique IPs in a given time period
It takes an Apache log file via stdin, the number of hours back you'd like to look -t (Default = 24 hours), and if you want the actual list of unique IPs -i

Options:
```
-h, --help  show this help message and exit
-i, --ips   shows list of unique IPs
-t HOURS    number of hours back you want to look
```

Usage Example:
```
python apacheCounter.py -i -t 48 < apache.log
