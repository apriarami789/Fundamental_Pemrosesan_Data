import pandas as pd
import re

# -------------Read data------------------
def read_data(data):
    try:
        df = pd.read_csv(data)
        return df
    except FileNotFoundError:
        print("nama file salah atau file tidak ditemukan")
        return None
    except pd.errors.ParserError:
        print("file data bukan berformat csv")
        return None
    except Exception as e:
        print(f"Terjadi error lain: {e}")
        return None


# -------------Transform Data-------------
# Transformasi kolom product_name
def extract_product_name(val):
    if pd.isna(val) or "Unknown Product" in val:
        return None
    return str(val)

# Transformasi kolom price
def extract_price(val):
    if pd.isna(val) or "Price Unavailable" in val:
        return None
    match = re.search(r"\$([\d\.]+)", str(val))
    return float(match.group(1)) if match else None

# Transformasi kolom rating
def extract_rating(val):
    if pd.isna(val) or "Not Rated" in str(val) or "Invalid Rating" in str(val):
        return None
    match = re.search(r"⭐ ([\d\.]+) / 5", str(val))
    return float(match.group(1)) if match else None

# Transformasi kolom color
def extract_color(val):
    match = re.search(r"(\d+) Colors", str(val))
    return int(match.group(1)) if match else None


# ---------Changes Data Type--------------
def change_data_type(data):
    """
    Mengubah tipe data kolom DataFrame menggunakan mapping.
    Juga menangani transformasi khusus untuk kolom tertentu.
    """
    # 1. Lakukan transformasi khusus yang tidak bisa dilakukan dengan astype biasa
    data['size'] = data['size'].str.replace('Size: ', '')
    data['gender'] = data['gender'].str.replace('Gender: ', '')

    # 2. Buat mapping untuk tipe data yang diinginkan
    #    Menggunakan 'Int64' (dengan huruf besar 'I') untuk integer
    #    memungkinkan adanya nilai NaN (missing values).
    dtype_mapping = {
        'product_name': 'string',
        'price': 'float64',
        'rating': 'float64',
        'color': 'Int64',
        'size': 'category',
        'gender': 'category'
    }

    # 3. Terapkan mapping ke DataFrame menggunakan astype()
    data = data.astype(dtype_mapping)

    # 4. Tangani kolom timestamp secara terpisah karena logikanya kondisional
    if 'scraped_at' in data.columns:
        data['scraped_at'] = pd.to_datetime(data['scraped_at'])
    else:
        # Fallback jika tidak ada kolom 'scraped_at'
        data['scraped_at'] = pd.Timestamp.now()

    print("Tipe data setiap kolom sudah diubah dan juga sudah di transformasi.")
    return data

# Pilih dan urutkan kolom akhir
def fix_column_data(data):
    try:
        df_transform = data[['product_name', 'price', 'rating', 'color', 'size', 'gender', 'scraped_at']]
        return df_transform
    except KeyError as e:
        print(f"Ada Kolom yang tidak ditemukan: {e}")
        return pd.DataFrame()


#--------------Clean Data-----------------
def clean_data(data):
    data = data.dropna().reset_index(drop=True)
    data = data.drop_duplicates().reset_index(drop=True)
    print("Data sudah dibersihkan dari nilai NaN dan duplikat.")
    return data

#----------------Convertion Data------------------
def dollar_to_rupiah(value):
    if pd.isna(value):
        return None
    return value * 16000

