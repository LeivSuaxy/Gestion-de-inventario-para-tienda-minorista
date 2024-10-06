from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class ProbandoApi(TestCase):
    def test_api(self):
        response = self.client.get(reverse('get_objects'))

        self.assertEqual(response.status_code, 200)

        response_json = response.json()

        self.assertIn('objects', response_json)
        self.assertIsInstance(response_json['objects'], list)
