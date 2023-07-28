#!/bin/bash
#python3 gen_index.py
#jq -r 'to_entries[]' out.json | jq -sr '.[0].value|.[]' > links
~/pi4/bin/tg.send_kd_line
