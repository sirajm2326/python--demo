import unittest
from unittest.mock import patch
from python--demo import app

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_get_skills(self):
        response = self.app.get('/api/skills')
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertIn('Python', data)
        self.assertIn('JavaScript', data)
        self.assertIn('SQL', data)

    @patch('python--demo.analyze_document_from_url')
    @patch(python--demo)
    @patch('python--demo.AzureSearchClient.search')
    def test_analyze_document(self, mock_search, mock_upload, mock_analyze):
        mock_search.return_value = {'result': 'mocked result'}
        mock_upload.return_value = None
        mock_analyze.return_value = {'response': 'mocked response'}

        data = {
            'context': 'Context example',
            'category': 'Category example',
            'threshold': 0.5,
            'noOfMatches': 5,
            'inputPath': 'https://example.com/document.pdf'
        }
        response = self.app.post('/analyze-document', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'response': 'mocked response'})

if __name__ == '__main__':
    unittest.main()
