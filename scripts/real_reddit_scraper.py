import urllib.request
import urllib.parse
import json
import time

subreddits = ['smallbusiness', 'sweatystartup', 'Construction', 'restaurantowners', 'realtors', 'bookkeeping', 'nursing', 'freelance']
real_complaints = []

print('Connecting to live Reddit JSON endpoints to pull 100% REAL data right now...\n')

for sub in subreddits:
    if len(real_complaints) >= 10:
        break
    print(f'Scraping r/{sub}...')
    url = f'https://www.reddit.com/r/{sub}/new.json?limit=100'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            children = data.get('data', {}).get('children', [])

            for child in children:
                post = child['data']
                title = post.get('title', '')
                text = post.get('selftext', '')
                url_str = 'https://reddit.com' + post.get('permalink', '')

                content = (title + ' ' + text).lower()

                signals = ['manually', 'spreadsheet', 'hate', 'software', 'app', 'nightmare', 'tracking', 'pain', 'client']
                matches = [s for s in signals if s in content]

                if len(matches) >= 2 and len(title) > 10 and not post.get('is_video'):
                    real_complaints.append({
                        'subreddit': sub,
                        'title': title,
                        'url': url_str,
                        'matches': matches
                    })

                if len(real_complaints) >= 10:
                    break
    except Exception as e:
        print(f'Failed to scrape r/{sub}: {e}')
    time.sleep(2)

print('\n' + '='*80)
print(f'FOUND {len(real_complaints)} REAL, LIVE THREADS CONTAINING PAIN SIGNALS:')
print('='*80)
for idx, c in enumerate(real_complaints):
    print(f"{idx+1}. [r/{c['subreddit']}] {c['title']}")
    print(f"   URL: {c['url']}")
    print(f"   Signals: {', '.join(c['matches'])}")
    print('-' * 80)
