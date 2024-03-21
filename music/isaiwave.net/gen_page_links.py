import os
import subprocess

for i in range(1, 34):
	print(i)
	os.system('rm out.html')
    if i==1:
	    cmd = '''wget -O out.html "https://isaiwave.net/songs/tamil-movie-songs/'''
    else:
        cmd = '''wget -O out.html "https://isaiwave.net/songs/tamil-movie-songs/page/''' + str(i) + '/"'
	os.system(cmd)
	cmd =  """ cat out.html | pup 'div[class="post-info"]' | pup 'a attr{href}' >> page_links"""
	subprocess.check_output(cmd, shell=True)
