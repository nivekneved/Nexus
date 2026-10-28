import urllib.request
import json
import re

def fetch_hn_stories(limit=30):
    print("Fetching top Ask HN stories from YCombinator API (100% REAL LIVE DATA)...\n")

    # 1. Fetch top Ask HN stories
    url = "https://hacker-news.firebaseio.com/v0/askstories.json"
    req = urllib.request.Request(url)

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            story_ids = json.loads(response.read().decode())[:limit]
    except Exception as e:
        print(f"Failed to fetch story IDs: {e}")
        return []

    complaints = []

    # 2. Analyze the stories and their top comments for pain points
    for idx, story_id in enumerate(story_ids):
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        try:
            with urllib.request.urlopen(urllib.request.Request(story_url), timeout=5) as s_res:
                story = json.loads(s_res.read().decode())

                title = story.get('title', '')
                text = story.get('text', '')

                content = (title + " " + text).lower()

                # We are looking for "Who wants X", "I wish", "Problem", "Hard to", "Seeking"
                pain_signals = ['wish', 'hard to', 'problem', 'looking for', 'manual', 'hate', 'spreadsheet']
                matches = [s for s in pain_signals if s in content]

                # If the title explicitly asks for solutions or has pain signals
                if matches or "ask hn" in title.lower() or "?" in title:
                    complaints.append({
                        'title': title,
                        'text': text[:200] + ("..." if len(text) > 200 else ""),
                        'url': f"https://news.ycombinator.com/item?id={story_id}",
                        'signals': matches,
                        'score': story.get('score', 0)
                    })
        except Exception:
            pass

    return sorted(complaints, key=lambda x: x['score'], reverse=True)

real_data = fetch_hn_stories(limit=40)

print("="*100)
print(f"FOUND {len(real_data)} REAL, LIVE REQUESTS ON HACKER NEWS TODAY:")
print("="*100)

for idx, c in enumerate(real_data):
    # Skip purely meta posts
    if "Who is hiring" in c['title'] or "freelancer" in c['title'].lower():
        continue

    print(f"\n💡 LEAD #{idx+1} | Score: {c['score']}")
    print(f"TITLE: {c['title']}")
    if c['text']:
        # clean up basic HTML
        clean_text = re.sub(r'<[^>]+>', '', c['text'])
        print(f"CONTEXT: {clean_text}")
    print(f"URL: {c['url']}")
    if c['signals']:
        print(f"SIGNALS: {', '.join(c['signals'])}")
    print("-" * 100)
