from unittest.mock import patch

from django.db import DatabaseError
from django.test import SimpleTestCase
from django.urls import reverse


class HealthEndpointTests(SimpleTestCase):
    databases = {'default'}

    def test_health_returns_ok_when_database_is_available(self):
        response = self.client.get(reverse('health'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})

    @patch('api.health.connection.cursor', side_effect=DatabaseError)
    def test_health_returns_503_when_database_is_unavailable(self, _cursor):
        response = self.client.get(reverse('health'))

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {'status': 'unhealthy'})
