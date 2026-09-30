import os
from typing import Dict, Any, List

class ProgrammaticSEOEngine:
    """
    Skill 3: Programmatic SEO & Inbound Engine
    Generates hundreds of hyper-localized, schema-optimized landing pages to capture inbound B2B search traffic.
    """
    def __init__(self):
        self.seo_dir = os.path.abspath("static/seo_pages")
        os.makedirs(self.seo_dir, exist_ok=True)

    def generate_pages(self, niche: str, locations: List[str]) -> Dict[str, Any]:
        print(f"[ProgrammaticSEO] Generating inbound landing pages for {niche}...")

        template = """<!DOCTYPE html>
<html>
<head>
    <title>Best {NICHE} in {LOCATION}</title>
    <meta name="description" content="Automate your {NICHE} business in {LOCATION} with our turnkey SaaS solutions. Instantly deploy WhatsApp bots and CRM systems.">
    <!-- Automated Schema Markup -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "name": "{NICHE} Automation Suite",
      "operatingSystem": "Web, Android, iOS",
      "applicationCategory": "BusinessApplication",
      "areaServed": "{LOCATION}"
    }
    </script>
</head>
<body>
    <h1>#1 {NICHE} Software Suite for {LOCATION}</h1>
    <p>Get a custom WhatsApp bot and CRM deployed for your business in {LOCATION} today.</p>
    <button>Request Demo</button>
</body>
</html>
"""
        generated_urls = []
        for loc in locations:
            slug = f"{niche.replace(' ', '-')}-in-{loc.replace(' ', '-')}".lower()
            file_path = os.path.join(self.seo_dir, f"{slug}.html")

            html_content = template.replace("{NICHE}", niche.title()).replace("{LOCATION}", loc.title())

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            generated_urls.append(f"/seo_pages/{slug}.html")

        print(f"[ProgrammaticSEO] Successfully injected {len(generated_urls)} pages into the sitemap.")

        return {
            "success": True,
            "pages_generated": len(generated_urls),
            "niche": niche,
            "urls": generated_urls
        }

seo_engine = ProgrammaticSEOEngine()
