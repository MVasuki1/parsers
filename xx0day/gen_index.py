#!/usr/bin/python3
import json
import os
import time
import subprocess
from collections import defaultdict
index_path = "https://xx0day.com/page/{0}/?filter=latest"

date_dict = defaultdict(list)

for i in range(1,11):
    os.system('rm /tmp/index.html*')
    os.system('wget -O /tmp/index.html ' + index_path.format(i))
    page_links = subprocess.check_output("""cat /tmp/index.html | pup 'div[class="videos-list"] article a attr{href}'""", shell=True).decode().strip().split("\n")
    with open('./page_links.txt', 'a') as f:
        f.write("\n".join(page_links) + "\n")
    uptobox_links = []
    for page_link in page_links:
        #uptobox_link = subprocess.check_output("""curl -s "{page_link}" | | grep -op 'https:\/\/uptobox.com/.*?(?=" rel)'""", shell=true).decode().strip()
        os.system('rm /tmp/page.html*')
        os.system('wget -O /tmp/page.html ' + page_link)
        vid_date = subprocess.check_output("""cat /tmp/page.html | pup 'div[id="video-date"] json{}' | jq -r '.[0].text'""", shell=True).decode()
        uptobox_link = subprocess.check_output("""cat /tmp/page.html | pup 'a[id="tracking-url"] attr{href}'""", shell=True).decode().strip()
        date_dict[vid_date].append(f"{page_link},{uptobox_link}")
    #with open('./uptobox_links.txt', 'a') as f:
    #    f.write("\n".join(uptobox_links) + "\n")

    #if i%5 == 0:
    #    time.sleep(5)

with open('out.json', 'w') as f:
    f.write(json.dumps(date_dict))
