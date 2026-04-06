import asyncio
import aiohttp
import json
import os
import sys
from aiohttp_socks import ProxyConnector

class WaybackURL:
    def __init__(self, domain, proxy="socks5://127.0.0.1:9050"):
        self.domain = domain.strip().lower()
        self.proxy = proxy
        # Target keywords for confidential/sensitive data leaks
        self.sensitive_patterns = [
            '.env', '.git', '.svn', '.config', 'web.config', 'settings.php',
            'config.php', 'database.sql', 'backup.sql', 'backup.zip', 'setup.php',
            'passwd', 'shadow', 'id_rsa', 'secret', 'key', 'token',
            'credentials', 'api_key', 'access_token', '.bak', '.old', 'hidden'
        ]
        self.found_leaks = []

    async def fetch_history(self):
        """Connects via Tor and queries the Wayback CDX API."""
        print(f"[*] Initializing Stealth Tunnel (Tor: {self.proxy})...")
        print(f"[*] Searching Wayback History for: {self.domain}...")

        # CDX API Query: *.domain/* fetches all subdomains and paths ever archived
        cdx_api = f"https://web.archive.org/cdx/search/cdx?url=*.{self.domain}/*&output=json&collapse=urlkey&fl=original,timestamp"

        connector = ProxyConnector.from_url(self.proxy)
        try:
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(cdx_api, timeout=45) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Skip the first item (headers)
                        if len(data) > 1:
                            self.filter_leaks(data[1:])
                        else:
                            print("[!] No historical records found for this domain.")
                    else:
                        print(f"[!] API Error: Received HTTP {response.status}")
        except Exception as e:
            print(f"[!] Connection Error: {e}\n[!] Ensure Tor service is running (sudo service tor start).")

    def filter_leaks(self, entries):
        """Filters the URL list for confidential file patterns."""
        print(f"[*] Scanning {len(entries)} archived URLs for confidential signatures...")
        
        for entry in entries:
            url, timestamp = entry[0], entry[1]
            
            # Identify if the URL contains any high-value patterns
            if any(pattern in url.lower() for pattern in self.sensitive_patterns):
                # Construct the raw 'id_' link to bypass the Wayback UI overlay
                raw_direct_link = f"https://web.archive.org/web/{timestamp}id_/{url}"
                
                self.found_leaks.append({
                    "file_name": url.split("/")[-1],
                    "original_location": url,
                    "direct_archive_link": raw_direct_link,
                    "archive_date": timestamp
                })

    def save_results(self, filename):
        """Saves the discovered links into a formatted .json file."""
        if not os.path.exists("reports"):
            os.makedirs("reports")

        output_path = os.path.join("reports", f"{filename}.json")
        
        report_data = {
            "target_website": self.domain,
            "leak_count": len(self.found_leaks),
            "confidential_links": self.found_leaks
        }

        with open(output_path, "w") as f:
            json.dump(report_data, f, indent=4)
        
        print("-" * 60)
        print(f"[+] Analysis Finished!")
        print(f"[+] Potentially Confidential Links: {len(self.found_leaks)}")
        print(f"[+] Results saved to: {output_path}")
        print("-" * 60)

async def main():
    print("\n" + "=" * 60)
    print("      WAYBACKURL v1.0 - CONFIDENTIAL DATA DISCOVERY")
    print("=" * 60)
    
    target_site = input("\nEnter your Website (e.g., target.com): ").strip()
    if not target_site:
        print("[!] Error: Website domain is required.")
        return

    json_filename = input("Enter output JSON filename (e.g., leak_report): ").strip()
    if not json_filename:
        json_filename = f"wayback_{target_site.replace('.', '_')}"

    scanner = WaybackURL(target_site)
    await scanner.fetch_history()
    scanner.save_results(json_filename)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Program closed by user.")
        sys.exit(0)