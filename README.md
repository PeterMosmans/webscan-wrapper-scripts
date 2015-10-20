# webscan-wrapper-scripts
A collection of short wrappers and utility scripts for scanning websites (on security vulnerabilities)


## wappalyzer_wrapper.py
A wrapper around Wappalyzer: Checks which framework(s) a (list of) website(s) use(s)


### Dependencies
* BeautifulSoup (needed by Wappalyzer)
* python-Wappalyzer
* requests


### Installation
pip install -r requirements.txt


### Usage
```
usage: wappalyzer_wrapper.py [-h] [--file FILE] [URL]


positional arguments:
  URL          the URL to check

optional arguments:
  -h, --help   show this help message and exit
  --file FILE  file containing urls to check
  ```
