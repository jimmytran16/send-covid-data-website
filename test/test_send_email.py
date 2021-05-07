import unittest
from application import application as app
from dotenv import load_dotenv
import os
load_dotenv()

# Test case for sending out the email
class TestSendEmailSubmissionEndpoint(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client() # get the client instance to use to test the endpoints
        self.email = os.getenv('EMAIL_TEST')

    def tearDown(self):
        pass

    def convert_byte_to_string(self,data):
        return data.decode("utf-8")

    # this should successfully send the email to the user
    # should return a 200 status
    def test_send_covid_submission_post_method(self):
        response = self.client.post('/submit', data=dict(
            email=self.email
        ), follow_redirects=True)
        response_content = self.convert_byte_to_string(response.data)  
 
        context_expected = "Successfully sent to {}".format(self.email)
        self.assertIn(context_expected,response_content)
        self.assertEqual(response.status_code, 200)
    
    # this should unsucessfully send an email since this endpoint is strictly a POST
    # should expect a 405 status code
    def test_send_covid_submission_get_method(self):
        response = self.client.get('/submit', data=dict(
            email=self.email
        ), follow_redirects=True)
        response_content = self.convert_byte_to_string(response.data)  
 
        context_expected = "The method is not allowed for the requested URL."
        self.assertIn(context_expected,response_content)
        self.assertEqual(response.status_code, 405)


        