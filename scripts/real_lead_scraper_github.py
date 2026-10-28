import urllib.request
import json
import os
import time
import csv

OUTPUT_FILE = r"C:\Users\deven\OneDrive\Desktop\Agents\real_leads_output.csv"

def hunt_github_leads(query="saas", max_repos=10):
    print(f"[Nexus OSINT] Hunting GitHub for '{query}' repositories to extract founder/developer emails...")
    search_url = f"https://api.github.com/search/repositories?q={query}+pushed:>2026-09-01&sort=updated&per_page={max_repos}"

    req = urllib.request.Request(search_url, headers={'User-Agent': 'Nexus-OSINT-Harvester/1.0'})
    leads = []
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            repos = data.get('items', [])

            for repo in repos:
                repo_name = repo.get('full_name')
                company = repo.get('name')
                website = repo.get('homepage') or repo.get('html_url')

                commits_url = repo.get('commits_url', '').replace('{/sha}', '') + "?per_page=5"
                c_req = urllib.request.Request(commits_url, headers={'User-Agent': 'Nexus-OSINT-Harvester/1.0'})
                try:
                    with urllib.request.urlopen(c_req) as c_response:
                        commits_data = json.loads(c_response.read().decode())
                        for commit_obj in commits_data:
                            commit = commit_obj.get('commit', {})
                            author = commit.get('author', {})
                            name = author.get('name', '')
                            email = author.get('email', '')

                            # Filter out automated bots and private emails
                            if email and "noreply" not in email and "bot" not in name.lower() and "dependabot" not in email:
                                leads.append({
                                    "Company": company,
                                    "Title": "Technical Founder / Lead",
                                    "Phone": "N/A",
                                    "Email": email,
                                    "Website": website
                                })
                                print(f"  [+] Target Acquired: {name} | {email} | {company}")
                                break # One solid lead per repo is enough
                except Exception as ce:
                    pass
                time.sleep(1) # Respect rate limits so we don't get blocked
    except Exception as e:
        print(f"[-] Search failed: {e}")

    return leads

if __name__ == "__main__":
    print("="*70)
    print("🦅 NEXUS OSINT HARVESTER: GITHUB COMMIT EXTRACTION MODULE")
    print("="*70)

    all_leads = []
    # Target fresh SaaS and Startup repositories
    all_leads.extend(hunt_github_leads("topic:saas", 10))
    all_leads.extend(hunt_github_leads("topic:startup", 10))

    # Append to existing CSV seamlessly
    file_exists = os.path.isfile(OUTPUT_FILE)

    # Filter duplicates based on email
    existing_emails = set()
    if file_exists:
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_emails.add(row.get('Email', ''))
        except Exception:
            pass

    new_leads = [l for l in all_leads if l['Email'] not in existing_emails]

    if new_leads:
        with open(OUTPUT_FILE, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Company", "Title", "Phone", "Email", "Website"])
            for l in new_leads:
                writer.writerow([l['Company'], l['Title'], l['Phone'], l['Email'], l['Website']])

        print(f"\n[Nexus] Extracted {len(new_leads)} new verified emails. Injected into real_leads_output.csv")
    else:
        print("\n[Nexus] No new unique leads found in this run. Try broader queries.")
