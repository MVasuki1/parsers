curl -s https://old.reddit.com/r/javdreams/.json | jq -r '.data.children[]| .data.preview.reddit_video_preview.fallback_url' | grep -v '^$' | grep -v null
