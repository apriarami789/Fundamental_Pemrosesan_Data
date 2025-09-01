import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def extract_fashion_data(item,scraped_at=None):
    """Mengekstrak data produk fashion dari satu elemen."""
    try:
        title = item.find("h3", {"class": "product-title"}).get_text(strip=True)
        price = item.find("span",{"class": "price"})
        product_detail = item.find_all("p")

        if price == None:
            price = item.find("p",{"class":"price"}).get_text(strip=True)
            rating = product_detail[1].get_text(strip=True)
            color = product_detail[2].get_text(strip=True)
            size = product_detail[3].get_text(strip=True)
            gender = product_detail[4].get_text(strip=True)
        else:
            price = price.get_text(strip=True)
            rating = product_detail[0].get_text(strip=True)
            color = product_detail[1].get_text(strip=True)
            size = product_detail[2].get_text(strip=True)
            gender = product_detail[3].get_text(strip=True)
    except (AttributeError, IndexError):
        # Jika ada error parsing, kembalikan dictionary kosong atau None
        return None

    return {
        "product_name": title,
        "price": price,
        "rating": rating,
        "color": color,
        "size": size,
        "gender": gender,
        "scraped_at": scraped_at if scraped_at else datetime.now().isoformat()
    }

def fetch_page_content(url):
    """Mengambil konten HTML dari URL yang diberikan."""
    try:
        session = requests.Session()
        response = session.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Akan raise error untuk status 4xx/5xx
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan ketika melakukan requests terhadap {url}: {e}")
        return None
    
def scrape_fashion_data(base_url, start_page=1, delay=2):
    """Fungsi utama untuk mengambil keseluruhan data, mulai dari requests hingga menyimpannya dalam variabel data."""
    data = []
    page_number = start_page
 
    while True:
        url = f"{base_url}page{page_number}" if page_number > 1 else base_url
        print(f"Scraping halaman: {url}")
            
        content = fetch_page_content(url)
        if content:
            soup = BeautifulSoup(content, "html.parser")
            product_details = soup.find_all("div", {"class": "collection-card"})

            if not product_details: # Berhenti jika tidak ada produk di halaman
                break

            for section in product_details:
                scraped_at = datetime.now().isoformat()
                fashion_data = extract_fashion_data(section,scraped_at=scraped_at)
                if fashion_data: # Hanya tambahkan jika data berhasil diekstrak
                    data.append(fashion_data)
 
            next_button = soup.find('li', class_='page-item next')
            if next_button and 'disabled' not in next_button.get('class', []):
                page_number += 1
                if delay > 0:
                    time.sleep(delay) # Delay sebelum halaman berikutnya
            else:
                break # Berhenti jika sudah tidak ada next button
        else:
            break # Berhenti jika ada kesalahan
 
    return data


def is_website_accessible(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error saat mengakses {url}: {e}")
        return False




    


