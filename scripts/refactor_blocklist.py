import os
import re
import ipaddress
from datetime import datetime

# Find the root directory relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
BLOCKLIST_PATH = os.path.join(ROOT_DIR, "lista_ads_brasil_pihole.txt")

def is_ip(val):
    try:
        ipaddress.ip_address(val)
        return True
    except ValueError:
        return False

def refactor():
    if not os.path.exists(BLOCKLIST_PATH):
        print(f"Error: {BLOCKLIST_PATH} not found.")
        return

    with open(BLOCKLIST_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()

    header_lines = []
    domains = set()

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            header_lines.append(stripped)
        elif stripped:
            if not is_ip(stripped):
                domains.add(stripped)

    sorted_domains = sorted(list(domains))
    total_count = len(sorted_domains)
    now = datetime.now().strftime("%d-%m-%Y %I:%M %p")

    new_content = []
    for line in header_lines:
        if line.startswith("# Last modified:"):
            new_content.append(f"# Last modified: {now}")
        elif line.startswith("# Total Sites Bloqueados:"):
            new_content.append(f"# Total Sites Bloqueados:  {total_count}")
        else:
            new_content.append(line)

    # Add blank lines after header
    new_content.append("")
    new_content.append("")
    new_content.append("")

    for domain in sorted_domains:
        new_content.append(domain)

    # Save with CRLF
    with open(BLOCKLIST_PATH, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\n".join(new_content) + "\n")

    print(f"Successfully refactored {BLOCKLIST_PATH}")

if __name__ == "__main__":
    refactor()
