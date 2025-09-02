import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
import requests
from utils import extract

class TestExtractModule(unittest.TestCase):
    def setUp(self):
        # HTML dengan <span class="price">
        self.html_with_span = '''
        <div class="collection-card">
            <h3 class="product-title">T-shirt 1</h3>
            <span class="price">$100.00</span>
            <p>Rating: ⭐ 4.5 / 5</p>
            <p>3 Colors</p>
            <p>Size: M</p>
            <p>Gender: Men</p>
        </div>
        '''
        # HTML tanpa <span class="price">
        self.html_without_span = '''
        <div class="collection-card">
            <h3 class="product-title">T-shirt 2</h3>
            <p class="price">$120.00</p>
            <p>Rating: ⭐ 3.9 / 5</p>
            <p>3 Colors</p>
            <p>Size: L</p>
            <p>Gender: Women</p>
        </div>
        '''

    def test_extract_fashion_data_with_span(self):
        soup = BeautifulSoup(self.html_with_span, "html.parser")
        item = soup.find("div", class_="collection-card")
        result = extract.extract_fashion_data(item, scraped_at="2025-08-29T19:23:21.333678")
        self.assertEqual(result['product_name'], "T-shirt 1")
        self.assertEqual(result['price'], "$100.00")
        self.assertEqual(result['rating'], "Rating: ⭐ 4.5 / 5")
        self.assertEqual(result['color'], "3 Colors")
        self.assertEqual(result['size'], "Size: M")
        self.assertEqual(result['gender'], "Gender: Men")
        self.assertEqual(result['scraped_at'], "2025-08-29T19:23:21.333678")

    def test_extract_fashion_data_without_span(self):
        soup = BeautifulSoup(self.html_without_span, "html.parser")
        item = soup.find("div", class_="collection-card")
        result = extract.extract_fashion_data(item, scraped_at="2025-08-29T19:23:21.333678")
        self.assertEqual(result['product_name'], "T-shirt 2")
        self.assertEqual(result['price'], "$120.00")
        self.assertEqual(result['rating'], "Rating: ⭐ 3.9 / 5")
        self.assertEqual(result['color'], "3 Colors")
        self.assertEqual(result['size'], "Size: L")
        self.assertEqual(result['gender'], "Gender: Women")
        self.assertEqual(result['scraped_at'], "2025-08-29T19:23:21.333678")

    @patch('utils.extract.requests.Session.get')
    def test_fetch_page_content_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"<html>test</html>"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        content = extract.fetch_page_content("http://dummy-url.com")
        self.assertEqual(content, b"<html>test</html>")

    @patch('utils.extract.requests.Session.get')
    def test_fetch_page_content_fail(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("Request failed")
        mock_get.return_value = mock_response
        content = extract.fetch_page_content("http://dummy-url.com")
        self.assertIsNone(content)

    @patch('utils.extract.fetch_page_content')
    def test_scrape_fashion_data(self, mock_fetch):
        # Simulasi satu halaman dengan satu produk
        html = '''
        <div class="collection-card">
            <h3 class="product-title">T-shirt 1</h3>
            <span class="price">$100.00</span>
            <p>Rating: ⭐ 4.5 / 5</p>
            <p>3 Colors</p>
            <p>Size: M</p>
            <p>Gender: Men</p>
        </div>
        '''
        soup = BeautifulSoup(f"<html><body>{html}</body></html>", "html.parser")
        mock_fetch.side_effect = [
            str.encode(str(soup)),  # Halaman pertama
            None                    # Halaman berikutnya (stop)
        ]
        data = extract.scrape_fashion_data("http://dummy-url.com", delay=0)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        self.assertIn('product_name', data[0])
        self.assertIn('scraped_at', data[0])

    @patch('utils.extract.requests.get')
    def test_is_website_accessible_true(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertTrue(extract.is_website_accessible("http://dummy-url.com"))

    @patch('utils.extract.requests.get')
    def test_is_website_accessible_false(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        # Tambahkan raise_for_status yang memunculkan error untuk status 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError
        mock_get.return_value = mock_response
        self.assertFalse(extract.is_website_accessible("http://dummy-url.com"))

    @patch('utils.extract.requests.get')
    def test_is_website_accessible_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        self.assertFalse(extract.is_website_accessible("http://dummy-url.com"))

if __name__ == '__main__':
    unittest.main()