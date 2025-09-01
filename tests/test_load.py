import unittest
import os
import pandas as pd
from utils import load

class TestLoadModule(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'col1': [1, 2],
            'col2': ['a', 'b']
        })
        self.empty_df = pd.DataFrame(columns=['col1', 'col2'])

    def tearDown(self):
        # Hapus file hasil test jika ada
        for fname in ['test_clean.csv', 'test_raw.csv']:
            if os.path.exists(fname):
                os.remove(fname)

    def test_save_clean_data(self):
        try:
            load.save_clean_data(self.df, file_name='test_clean.csv')
            self.assertTrue(os.path.exists('test_clean.csv'))
            df_loaded = pd.read_csv('test_clean.csv')
            self.assertEqual(len(df_loaded), 2)
        except Exception as e:
            import traceback
            tb = traceback.extract_tb(e.__traceback__)
            print(f"Error at line {tb[-1].lineno}: {e}")
            raise

    def test_save_raw_data_with_data(self):
        try:
            load.save_raw_data(self.df, file_name='test_raw.csv')
            self.assertTrue(os.path.exists('test_raw.csv'))
            df_loaded = pd.read_csv('test_raw.csv')
            self.assertEqual(len(df_loaded), 2)
        except Exception as e:
            import traceback
            tb = traceback.extract_tb(e.__traceback__)
            print(f"Error at line {tb[-1].lineno}: {e}")
            raise

    def test_save_raw_data_empty(self):
        try:
            load.save_raw_data(self.empty_df, file_name='test_raw.csv')
            # File tidak dibuat jika DataFrame kosong
            self.assertFalse(os.path.exists('test_raw.csv'))
        except Exception as e:
            import traceback
            tb = traceback.extract_tb(e.__traceback__)
            print(f"Error at line {tb[-1].lineno}: {e}")
            raise

if __name__ == '__main__':
    unittest.main()