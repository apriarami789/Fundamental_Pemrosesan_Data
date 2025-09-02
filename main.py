from utils import extract, transform, load
import pandas as pd


def main():
    # URL awal
    url = 'https://fashion-studio.dicoding.dev/'
    if extract.is_website_accessible(url) is True:
        base_url = url
        print(f"Website {url} dapat diakses.")
    else:
        while True:
            url = input("Masukkan URL situs web yang akan di scraping: ")
            if extract.is_website_accessible(url) is True:
                print(f"Website {url} dapat diakses.")
                base_url = url
                break
            else:
                print(f"Website {url} tidak dapat diakses. Silakan masukkan URL yang valid.")

    
    fashion_data = extract.scrape_fashion_data(base_url,delay=0.2)
    df = pd.DataFrame(fashion_data)
    print(df)
    
    # Menyimpan raw data
    load.save_raw_data(df)

    # Fungsi untuk transform data
    df['product_name'] = df['product_name'].apply(transform.extract_product_name)
    df['price'] = df['price'].apply(transform.extract_price)
    df['rating'] = df['rating'].apply(transform.extract_rating)
    df['color'] = df['color'].apply(transform.extract_color)

    # fungsi konversi mata uang
    df['price'] = df['price'].apply(transform.dollar_to_rupiah)

    # Fungsi mengubah data type semua kolom
    df = transform.change_data_type(df)

    # Fungsi mengambil kolom yang penting
    df = transform.fix_column_data(df)
    
    # Fungsi untuk membersihkan data
    df = transform.clean_data(df)

    # Memberikan informasi setiap kolom
    df.info()

    # Fungsi menyimpan data ke CSV
    load.save_clean_data(df)

if __name__ == "__main__":
    main()