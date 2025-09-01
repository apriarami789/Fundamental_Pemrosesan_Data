def save_clean_data(data,file_name='clean_fashion_data.csv'):
    data.to_csv(file_name, index=False)
    print(f"Data telah disimpan ke '{file_name}'.")

def save_raw_data(df,file_name='fashion_data.csv'):
    if not df.empty:
        df.to_csv(file_name, index=False)
        print(f"Data telah disimpan ke '{file_name}'.")
    else:
        print("Tidak ada data yang ditemukan.")