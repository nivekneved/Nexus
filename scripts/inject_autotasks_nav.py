import os
from pathlib import Path

def inject_nav():
    static_dir = Path("static")
    nav_snippet = """          <!-- Auto Tasks -->
          <a href="/auto-tasks" class="nav-item" id="navItemAutoTasks" title="Auto Tasks & Autonomous Execution">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
            <span>⚡ Auto Tasks</span>
          </a>"""

    target_marker = "<span>5. Quote & Invoice</span>\n          </a>"

    count = 0
    for html_file in static_dir.glob("*.html"):
        if html_file.name == "auto_tasks.html":
            continue

        content = html_file.read_text(encoding="utf-8")
        if "navItemAutoTasks" in content:
            print(f"Skipping {html_file.name} (already has Auto Tasks)")
            continue

        if "<span>5. Quote & Invoice</span>" in content:
            # Find the anchor tag ending after quote & invoice
            # We can replace the quote & invoice block with quote & invoice + auto tasks
            marker = '<span>5. Quote & Invoice</span>\n          </a>'
            replacement = marker + "\n\n" + nav_snippet
            if marker in content:
                new_content = content.replace(marker, replacement, 1)
                html_file.write_text(new_content, encoding="utf-8")
                print(f"✅ Injected Auto Tasks into {html_file.name}")
                count += 1
            else:
                print(f"⚠️ Marker not found exact in {html_file.name}")

    print(f"\nSuccessfully injected Auto Tasks navigation link into {count} HTML files.")

if __name__ == "__main__":
    inject_nav()
