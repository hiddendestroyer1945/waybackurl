WaybackURL v1.0

WaybackURL is a high-performance OSINT (Open Source Intelligence) tool developed for Debian-based Linux systems. It is designed to perform "Digital Archeology" by querying the Internet Archive’s Wayback Machine to uncover subdomains, forgotten directory paths, and sensitive historical data leaks.

By utilizing the Wayback CDX API and routing all traffic through the Tor Network, WaybackURL identifies "ghost" files—such as private keys, database configurations, and environment files—that were once public and remain indexed in the global archive.

🛡️ Core Features

    Tor Stealth Integration: Native SOCKS5 proxy support ensures your origin IP is never exposed to the Internet Archive.

    Deep Heuristic Scanning: Automatically filters thousands of historical URLs for 20+ high-value sensitive patterns:

        Secrets: .env, config.php, settings.json, .git/config

        Backups: .sql, .bak, .zip, .tar.gz

        Credentials: id_rsa, api_key, access_token, passwd

    Wildcard Discovery: Uses *.target.com/* logic to map the entire historical attack surface, including subdomains.

    Direct Archive Links: Generates specialized id_ links that bypass the Wayback Machine’s web interface to provide raw, untouched file content.

    Asynchronous Engine: Built on aiohttp for rapid, parallel processing of massive datasets.

📋 Prerequisites

This tool is designed for Debian, Kali Linux, Ubuntu, or Parrot OS.
    Install & Start Tor:  

```Bash

    sudo apt update && sudo apt install tor python3-venv -y
    sudo service tor start
```

    - Python 3.10+ (Standard on most modern Debian distros).

🚀 Installation & Environment Setup

It is highly recommended to use a Python Virtual Environment to avoid conflicts with system libraries.
1. Clone the Repository
```Bash

git clone https://github.com/hiddendestroyer1945/waybackurl.git
cd waybackurl
```

2. Create and Activate Virtual Environment


# Create the virtual environment named 'venv'
```Bash
python3 -m venv venv
```

# Activate the environment
```Bash
source venv/bin/activate
```

Note: Your terminal prompt should now show (venv) at the beginning.
3. Install Dependencies
```Bash

pip install -r requirements.txt
```

## 🛠️ Usage

Ensure the Tor service is running: sudo service tor status

Ensure your virtual environment is active: source venv/bin/activate

## Launch the program:
```Bash

    python3 waybackurl.py
```
## Follow the interactive prompts:

        Enter your Website: e.g., example.com

        Enter output JSON filename: e.g., recon_results

📂 Output Format

Results are saved as a structured .json file in the reports/ directory.
JSON

{
    "target_website": "example.com",
    "leak_count": 1,
    "confidential_links": [
        {
            "file_name": ".env",
            "original_location": "http://example.com/.env",
            "direct_archive_link": "https://web.archive.org/web/20220101123000id_/http://example.com/.env",
            "archive_date": "20220101123000"
        }
    ]
}

⚖️ Disclaimer

This tool is intended for authorized security auditing, bug bounty hunting, and educational purposes only. The developer assumes no liability for misuse or damage caused by this program. Always obtain permission before performing reconnaissance on a target.

## Author

hiddendestroyer1945