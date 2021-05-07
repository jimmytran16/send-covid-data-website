import unittest
from application import application as app

class TestMainPage(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client() # get the client instance to use to test the endpoints

    def tearDown(self):
        pass

    def convert_byte_to_string(self,data):
        return data.decode("utf-8")

    def test_landing_page_response_status_200(self):
        response = self.client.get('/')
        response_content = self.convert_byte_to_string(response.data)

        self.assertEqual(response.status_code,200)
        self.assertIn("Get The Latest",response_content)
        self.assertIn("COVID-19",response_content)

    def test_landing_page_response_context(self):
        response = self.client.get('/')
        response_content = self.convert_byte_to_string(response.data)

        self.assertIn("Get The Latest",response_content)
        self.assertIn("COVID-19",response_content)