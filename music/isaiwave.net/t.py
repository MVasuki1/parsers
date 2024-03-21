import os
import subprocess

# Create folders for each page with a file 'links' containing all mp3 links in page

curl_cmd = """
curl 'https://food-foods.com/download.php' \
  -H 'authority: food-foods.com' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: en-GB,en;q=0.9' \
  -H 'cookie: PHPSESSID=grh9l71gibeisbdnlv2ig51opi; mid={mid}' \
  -H 'referer: https://isaiwave.net/' \
  -H 'sec-ch-ua: "Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: document' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-user: ?1' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'"""

with open('./links', 'r') as f:
	url_links_list = f.read().strip().split('\n')

for url in url_links_list:
	dirname = os.path.basename(url[:-1])
	os.system(f'mkdir "{dirname}"')
	file_ids = subprocess.check_output(f'curl "{url}" | ' +  "pup 'a attr{href}' | grep download.php | ggrep -oP '(?<=fileid=).*'", shell=True).decode().strip().split('\n')
	mp3_urls = []
	for file_id in file_ids:
		mp3_urls.append(subprocess.check_output(curl_cmd.format(mid=file_id) + " | pup 'a attr{href}' | tail -n 1 ", shell=True).decode().strip())
	with open(f'./{dirname}/links', 'w') as f:
		f.write('\n'.join(mp3_urls))
		
