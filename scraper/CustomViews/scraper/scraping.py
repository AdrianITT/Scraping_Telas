# scraper/scraping.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {"User-Agent": "Mozilla/5.0"}
BASE_URL = "https://modatelas.com.mx/"

def scrape_modatelas_core():
    """
    Hace el scraping y regresa una lista con los datos.
    """
    resp = requests.get(BASE_URL, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    data = []

    sections = soup.select(".menu-section")
    for section in sections:
        header = section.select_one(".section-header h3")
        if not header:
            continue

        section_name = header.get_text(strip=True)
        content = section.select_one(".section-content")
        if not content:
            continue

        sub_list = content.select_one(".subcategory-list")
        if not sub_list:
            continue

        for li in sub_list.find_all("li", recursive=False):
            div_parent = li.select_one("div.has-children")
            a_direct = li.find("a", recursive=False)

            # Grupo con nested list (Telas Más Buscadas)
            if div_parent:
                for icon in div_parent.select("i"):
                    icon.decompose()
                group_name = div_parent.get_text(strip=True)

                nested_ul = li.select_one("ul.nested-list")
                if nested_ul:
                    for sub_li in nested_ul.find_all("li", recursive=False):
                        a = sub_li.find("a")
                        if not a:
                            continue
                        for icon in a.select("i"):
                            icon.decompose()
                        item_name = a.get_text(strip=True)
                        href = a.get("href")
                        if href and not href.startswith("http"):
                            href = urljoin(BASE_URL, href)

                        data.append({
                            "section": section_name,
                            "group": group_name,
                            "name": item_name,
                            "url": href,
                        })

            # Subcategoría simple (Foami, etc.)
            elif a_direct:
                for icon in a_direct.select("i"):
                    icon.decompose()
                sub_name = a_direct.get_text(strip=True)
                href = a_direct.get("href")
                if href and not href.startswith("http"):
                    href = urljoin(BASE_URL, href)

                data.append({
                    "section": section_name,
                    "group": None,
                    "name": sub_name,
                    "url": href,
                })

    return data
