import subprocess
import sys
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings



#First populate the database with the most up to date info
process = CrawlerProcess(get_project_settings())
process.crawl("bandsspider")
process.start()  # the script will block here until the crawling is finished


#Paths to files to run. In order for post processing
scripts = ["./FilteringEvents/eventfilter.py", "./Email/formatmessage.py",  "./Email/send.py"]


for script in scripts:
    print(f"Running {script}...")
    process = subprocess.Popen(['python', script])
    return_code = process.wait()  # Wait for the script to finish
    if return_code != 0:
        print(f"Error: {script} failed with return code {return_code}. Exiting.")
        sys.exit(1)  # Exit the script with a non-zero exit code
    print(f"{script} finished.\n")