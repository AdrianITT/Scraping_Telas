import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

BASE_URL = "https://modatelas.com.mx/"

def scrape_modatelas():
    print("Scrapeando página principal de Modatelas...")
    resp = requests.get(BASE_URL, headers=HEADERS, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    
    sections = soup.select(".menu-section")
    
    print("Categorías encontradas:")
    for section in sections:
        # 👉 Nombre de la sección principal (Telas, Mercería, etc.)
        header = section.select_one(".section-header h3")
        if not header:
            continue
        
        section_name = header.get_text(strip=True)
        print(f"\n=== Sección: {section_name} ===")

        # 👉 Contenido asociado a esa sección
        content = section.select_one(".section-content")
        if not content:
            continue

        sub_list = content.select_one(".subcategory-list")
        if not sub_list:
            continue

        # Solo <li> directos (no los anidados)
        for li in sub_list.find_all("li", recursive=False):
            div_parent = li.select_one("div.has-children")
            a_direct = li.find("a", recursive=False)  # enlace directo (Foami, etc.)

            # 🔹 CASO 1: grupo con sublista (Telas Más Buscadas)
            if div_parent:
                # quitar iconos dentro del título del grupo
                for icon in div_parent.select("i"):
                    icon.decompose()
                group_name = div_parent.get_text(strip=True)
                print(f" - Grupo: {group_name}")

                nested_ul = li.select_one("ul.nested-list")
                if nested_ul:
                    # li internos dentro del grupo
                    for sub_li in nested_ul.find_all("li", recursive=False):
                        a = sub_li.find("a")
                        if not a:
                            continue
                        # quitar iconos del enlace interno
                        for icon in a.select("i"):
                            icon.decompose()
                        item_name = a.get_text(strip=True)
                        href = a.get("href")
                        if href and not href.startswith("http"):
                            href = urljoin(BASE_URL, href)
                        print(f"    * {item_name} -> {href}")

            # 🔹 CASO 2: subcategoria simple con enlace directo (Foami, etc.)
            elif a_direct:
                for icon in a_direct.select("i"):
                    icon.decompose()
                sub_name = a_direct.get_text(strip=True)
                href = a_direct.get("href")
                if href and not href.startswith("http"):
                    href = urljoin(BASE_URL, href)
                print(f" - {sub_name} -> {href}")


if __name__ == "__main__":
    scrape_modatelas()
