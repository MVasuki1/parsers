#!/usr/bin/python3
import pytz
import json
import os
import time
from dateutil import parser
from datetime import datetime, timedelta
import subprocess
from collections import defaultdict

def gen_xml_from_list(l: list, title: str):
    xml=f"<rss>\n<channel>\n<title>{title}</title>"
    for r in l:
        e = "\n".join([f'<{key}>{value}</{key}>' for key, value in r.items()])
        row_xml = f"<item>\n{e}\n</item>"
        xml = xml + "\n" + row_xml
    xml = xml + "\n</channel>\n</rss>" 
    return xml       


index_path = "https://xx0day.com/page/{0}/?filter=latest"
rss_list = []
three_hours_ago = datetime.now(pytz.utc) - timedelta(hours=3)
break_outer = False
for i in range(1,8):
    os.system('rm /tmp/index.html*')
    os.system('wget -cq -O /tmp/index.html ' + index_path.format(i))
    page_links = subprocess.check_output("""cat /tmp/index.html | pup 'div[class="videos-list"] article a attr{href}'""", shell=True).decode().strip().split("\n")
    #with open('./page_links.txt', 'a') as f:
    #    f.write("\n".join(page_links) + "\n")
    uptobox_links = []
    for page_link in page_links:
        #uptobox_link = subprocess.check_output("""curl -s "{page_link}" | | grep -op 'https:\/\/uptobox.com/.*?(?=" rel)'""", shell=true).decode().strip()
        os.system('rm /tmp/page.html*')
        os.system('wget -cq -O /tmp/page.html ' + page_link)
        vid_title = subprocess.check_output("""cat /tmp/page.html | pup 'meta[property="og:title"] attr{content}'""", shell=True).decode().strip().split('\n')[0]
        published_time_str = subprocess.check_output("""cat /tmp/page.html | pup 'meta[property="article:modified_time"] attr{content}'""", shell=True).decode().strip()
        published_time = parser.parse(published_time_str)
        uptobox_link = subprocess.check_output("""cat /tmp/page.html | pup 'a[id="tracking-url"] attr{href}'""", shell=True).decode().strip()
        if published_time < three_hours_ago:
            break_outer = True
            break
        else:
            rss_list.append({"title": vid_title, "link": uptobox_link, "pubDate": published_time_str})
        #vid_date = subprocess.check_output("""cat /tmp/page.html | pup 'div[id="video-date"] json{}' | jq -r '.[0].text'""", shell=True).decode()
        #date_dict[vid_date].append(f"{page_link},{uptobox_link}")
    #with open('./uptobox_links.txt', 'a') as f:
    #    f.write("\n".join(uptobox_links) + "\n")
    
    if break_outer:
        break

rss_feed = gen_xml_from_list(rss_list, "xx0day" + three_hours_ago.strftime("%Y-%m-%d %H:%M"))
with open("./three_hour_feed.rss", "w") as f:
    f.write(rss_feed)
