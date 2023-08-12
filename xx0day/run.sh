#!/bin/bash
#python3 gen_index.py
#jq -r 'to_entries[]' out.json | jq -sr '.[0].value|.[]' > links
#~/pi4/bin/tg.send_kd_line
#rm links

python3 gen_rss.py
git add three_hour_feed.rss
git commit -m "$(date)"
git push
