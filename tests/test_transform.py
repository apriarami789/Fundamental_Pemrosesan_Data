import unittest
import pandas as pd
from utils import transform

class TestTransformModule(unittest.TestCase):
    def setUp(self):
        self.raw_data = pd.DataFrame({
            'product_name': ['T-shirt 1', 'Unknown Product', None],
            'price': ['$100.00', 'Price Unavailable', '$200.00'],
            'rating': ['Rating: ⭐ 4.5 / 5', 'Rating: Not Rated', 'Rating: ⭐ Invalid Rating / 5'],
            'color': ['3 Colors', '8 Colors', None],
            'size': ['Size: M', 'Size: L', 'Size: XL'],
            'gender': ['Gender: Men', 'Gender: Women', 'Gender: Unisex'],
            'scraped_at': ['2025-08-29T19:23:21.333678']*3
        })

    def test_extract_product_name(self):
        self.assertEqual(transform.extract_product_name('T-shirt 1'), 'T-shirt 1')
        self.assertIsNone(transform.extract_product_name('Unknown Product'))
        self.assertIsNone(transform.extract_product_name(None))

    def test_extract_price(self):
        self.assertEqual(transform.extract_price('$100.00'), 100.00)
        self.assertIsNone(transform.extract_price('Price Unavailable'))
        self.assertIsNone(transform.extract_price(None))

    def test_extract_rating(self):
        self.assertEqual(transform.extract_rating('Rating: ⭐ 4.5 / 5'), 4.5)
        self.assertIsNone(transform.extract_rating('Rating: Not Rated'))
        self.assertIsNone(transform.extract_rating('Rating: ⭐ Invalid Rating / 5'))
        self.assertIsNone(transform.extract_rating(None))

    def test_extract_color(self):
        self.assertEqual(transform.extract_color('3 Colors'), 3)
        self.assertEqual(transform.extract_color('8 Colors'), 8)
        self.assertIsNone(transform.extract_color(None))

    def test_change_data_type(self):
        df = self.raw_data.copy()
        df['price'] = df['price'].apply(transform.extract_price)
        df['rating'] = df['rating'].apply(transform.extract_rating)
        df['color'] = df['color'].apply(transform.extract_color)
        try:
            df2 = transform.change_data_type(df)
            self.assertTrue(pd.api.types.is_float_dtype(df2['price']))
            self.assertTrue(pd.api.types.is_float_dtype(df2['rating']))
            self.assertTrue(pd.api.types.is_integer_dtype(df2['color']))
            self.assertTrue(pd.api.types.is_categorical_dtype(df2['size']))
            self.assertTrue(pd.api.types.is_categorical_dtype(df2['gender']))
            self.assertTrue(pd.api.types.is_datetime64_any_dtype(df2['timestamp']))
        except Exception as e:
            import traceback
            tb = traceback.extract_tb(e.__traceback__)
            print(f"Error at line {tb[-1].lineno}: {e}")
            raise

    def test_fix_column_data(self):
        df = self.raw_data.copy()
        df['price'] = df['price'].apply(transform.extract_price)
        df['rating'] = df['rating'].apply(transform.extract_rating)
        df['color'] = df['color'].apply(transform.extract_color)
        df = transform.change_data_type(df)
        try:
            df2 = transform.fix_column_data(df)
            self.assertListEqual(
                list(df2.columns),
                ['product_name', 'price', 'rating', 'color', 'size', 'gender', 'timestamp']
            )
        except Exception as e:
            import traceback
            tb = traceback.extract_tb(e.__traceback__)
            print(f"Error at line {tb[-1].lineno}: {e}")
            raise

    def test_clean_data(self):
        df = pd.DataFrame({
            'product_name': ['A', 'A', None],
            'price': [1, 1, 2],
            'rating': [4.0, 4.0, None],
            'color': [3, 3, 4],
            'size': ['M', 'M', 'L'],
            'gender': ['Men', 'Men', 'Women'],
            'timestamp': pd.to_datetime(['2025-08-29T19:23:21.333678']*3)
        })
        try:
            df_clean = transform.clean_data(df)
            self.assertEqual(len(df_clean), 1)
            self.assertFalse(df_clean.isnull().any().any())
        except Exception as e:
            import traceback
            tb = traceback.extract_tb(e.__traceback__)
            print(f"Error at line {tb[-1].lineno}: {e}")
            raise

    def test_dollar_to_rupiah(self):
        self.assertEqual(transform.dollar_to_rupiah(2), 32000)
        self.assertIsNone(transform.dollar_to_rupiah(None))

if __name__ == '__main__':
    unittest.main()