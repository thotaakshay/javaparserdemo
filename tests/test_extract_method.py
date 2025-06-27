import unittest
from unittest.mock import patch, Mock

from extract_method import extract_method

class TestExtractMethod(unittest.TestCase):
    @patch('subprocess.run')
    def test_extract_method_success(self, mock_run):
        mock_run.return_value = Mock(returncode=0, stdout='method code\n', stderr='')
        result = extract_method('Dummy.java')
        self.assertEqual(result, 'method code')
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_extract_method_error(self, mock_run):
        mock_run.return_value = Mock(returncode=1, stdout='', stderr='error')
        result = extract_method('Dummy.java')
        self.assertIsNone(result)
        mock_run.assert_called_once()

if __name__ == '__main__':
    unittest.main()
