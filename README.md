# python-absolubot
A python with selenium bot for web scraping of Absolut drink recipes from http://www.absolut.com

# Requirements
* python3
* python selenium lib
* chromedriver (or similar)

# How to install (Linux)

**Step 1:** Download chromedriver (or similar) and put it on /usr/bin/chromedriver

**Step 2:** Install the selenium-python library (Debian)
```
pip install selenium
```

# Usage 

**Example 1:** 
This command below will start the scraping process with timeout in 20 and sleep time in 1 second. Also, the output will be generate to output.txt.
```
python3 main.py -t 20 -s 1 -o output.txt
```

