from django.test import TestCase
from django.urls import reverse

class GetFeedbackEndpointTest(TestCase):

    def test_get_feedback_GET_405(self):
        """
        The get_feedback view function should only work for POST requests.
        A GET request should return a 405 (method not allowed)
        """
        response = self.client.get(reverse('notifications:get_feedback'))
        self.assertEqual(response.status_code, 405)

    def test_get_feedback_POST(self):
        """
        Posting content returns a 302 (URL redirect)
        """
        response = self.client.post(reverse('notifications:get_feedback'), {'name':'Jeremie'})
        self.assertEqual(response.status_code, 302)
