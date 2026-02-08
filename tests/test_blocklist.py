import pytest
import re
import os
import ipaddress

# Find the root directory relative to this test file
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(TEST_DIR)
BLOCKLIST_PATH = os.path.join(ROOT_DIR, "lista_ads_brasil_pihole.txt")

def is_ip(val):
    try:
        ipaddress.ip_address(val)
        return True
    except ValueError:
        return False

def get_domains():
    domains = []
    if not os.path.exists(BLOCKLIST_PATH):
        return domains
    with open(BLOCKLIST_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                domains.append(line)
    return domains

def get_header_count():
    if not os.path.exists(BLOCKLIST_PATH):
        return None
    with open(BLOCKLIST_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("# Total Sites Bloqueados:"):
                try:
                    return int(line.split(":")[-1].strip())
                except ValueError:
                    return None
    return None

def test_sorted():
    domains = get_domains()
    assert domains, "No domains found in blocklist"
    assert domains == sorted(domains), "Blocklist is not sorted alphabetically"

def test_unique():
    domains = get_domains()
    seen = set()
    duplicates = []
    for d in domains:
        if d in seen:
            duplicates.append(d)
        else:
            seen.add(d)
    assert len(domains) == len(seen), f"Blocklist contains duplicate entries: {duplicates[:10]}"

def test_no_ips():
    domains = get_domains()
    ips = [d for d in domains if is_ip(d)]
    assert not ips, f"Blocklist contains IP addresses (IPv4 or IPv6): {ips[:10]}"

def test_header_count():
    domains = get_domains()
    header_count = get_header_count()
    assert header_count == len(domains), f"Header count ({header_count}) does not match actual domain count ({len(domains)})"
