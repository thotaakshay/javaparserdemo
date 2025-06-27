import unittest
import importlib.util
from unittest.mock import patch

FLASK_AVAILABLE = importlib.util.find_spec("flask") is not None

@unittest.skipUnless(FLASK_AVAILABLE, "Flask not installed")
class TestApp(unittest.TestCase):
    def setUp(self):
        from app import app  # Import here so Flask is required only if installed
        self.client = app.test_client()

    @patch('app.extract_method')
    @patch('app.generate_junit_test')
    def test_generate_endpoint(self, mock_generate, mock_extract):
        from app import app
        mock_extract.return_value = 'method code'
        mock_generate.return_value = 'junit code'
        response = self.client.post('/generate', json={'file_path': 'Dummy.java'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'junit_test': 'junit code'})

    @patch('app.generate_junit_test')
    def test_generate_tests_endpoint(self, mock_generate):
        from app import app
        mock_generate.return_value = 'junit code'
        payload = {
            'files': [
                {'name': 'Example.java', 'content': 'class Example {}'}
            ]
        }
        response = self.client.post('/generate-tests', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/zip')
        import io, zipfile
        zf = zipfile.ZipFile(io.BytesIO(response.data))
        self.assertIn('ExampleTest.java', zf.namelist())
        self.assertEqual(zf.read('ExampleTest.java').decode(), 'junit code')


if __name__ == '__main__':
    unittest.main()
