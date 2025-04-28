#!/usr/bin/env python3
import sys
import cloudscraper
from bs4 import BeautifulSoup
import re

BASE_URL = "https://istheservicedown.com.br/status/"

def get_service_code(service_slug):
    scraper = cloudscraper.create_scraper()
    url = f"{BASE_URL}{service_slug}"
    try:
        response = scraper.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        full_text = soup.get_text(separator=' ', strip=True).lower()

        if "nenhum problema detectado" in full_text or f"o {service_slug} está funcionando normalmente" in full_text:
            return 0
        elif "alguns problemas detectados" in full_text:
            return 1
        elif "problemas detectados" in full_text or re.search(rf"o {service_slug} está enfrentando (problemas|interrupções)", full_text):
            return 2
        return 3
    except:
        return 3

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("-1")
        sys.exit(1)

    slug = sys.argv[1]
    result = get_service_code(slug)
    print(result)