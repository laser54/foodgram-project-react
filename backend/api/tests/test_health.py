from unittest.mock import patch

from django.db import DatabaseError
from django.test import SimpleTestCase, override_settings
from django.urls import reverse


@override_settings(ALLOWED_HOSTS=['foodgram.larin.work'])
class HealthEndpointTests(SimpleTestCase):
    databases = {'default'}

    def test_health_returns_ok_when_database_is_available(self):
        response = self.client.get(
            reverse('health'), HTTP_HOST='foodgram.larin.work'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})

    @patch('api.health.connection.cursor', side_effect=DatabaseError)
    def test_health_returns_503_when_database_is_unavailable(self, _cursor):
        response = self.client.get(
            reverse('health'), HTTP_HOST='foodgram.larin.work'
        )

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {'status': 'unhealthy'})

    @patch('api.health.connection.cursor')
    def test_health_rejects_unlisted_loopback_host(self, cursor):
        response = self.client.get(
            reverse('health'), HTTP_HOST='127.0.0.1:8000'
        )

        self.assertEqual(response.status_code, 400)
        cursor.assert_not_called()
