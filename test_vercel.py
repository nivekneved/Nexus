import urllib.request
import urllib.error

url = "https://nexusbots-nu.vercel.app/api/status"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

try:
    with urllib.request.urlopen(req) as resp:
        print("STATUS:", resp.status)
        print("BODY:", resp.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    print("CODE:", e.code)
    print("HEADERS:", dict(e.headers))
    print("BODY:", e.read().decode("utf-8", errors="replace"))
except Exception as ex:
    print("EXCEPTION:", ex)
