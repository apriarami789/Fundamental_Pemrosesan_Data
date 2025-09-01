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
    return val

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
    df = data.copy()
    df['product_name'] = df['product_name'].astype(str)
    df['price'] = df['price'].astype('Float64')
    df['rating'] = df['rating'].astype('Float64')
    df['color'] = df['color'].astype('Int64')
    df['size'] = df['size'].str.replace('Size: ', '').astype('category')
    df['gender'] = df['gender'].str.replace('Gender: ', '').astype('category')
    # Pastikan kolom scraped_at ada
    if 'scraped_at' in df.columns:
        df['timestamp'] = pd.to_datetime(df['scraped_at'])
    elif 'timestamp' not in df.columns:
        # fallback jika tidak ada scraped_at, buat timestamp dummy
        df['timestamp'] = pd.Timestamp.now()
    print("Tipe data setiap kolom sudah diubah dan juga sudah di transformasi.")
    return df

# Pilih dan urutkan kolom akhir
def fix_column_data(data):
    try:
        df_transform = data[['product_name', 'price', 'rating', 'color', 'size', 'gender', 'timestamp']]
        return df_transform
    except KeyError as e:
        print(f"Ada Kolom yang tidak ditemukan: {e}")
        return pd.DataFrame()


#--------------Clean Data-----------------
def clean_data(data):
    df_clean = data.dropna().reset_index(drop=True)
    df_clean = df_clean.drop_duplicates().reset_index(drop=True)
    print("Data sudah dibersihkan dari nilai NaN dan duplikat.")
    return df_clean

#----------------Convertion Data------------------
def dollar_to_rupiah(value):
    if pd.isna(value):
        return None
    return value * 16000

