from django.db import DatabaseError, connection
from django.http import JsonResponse


def health(request):
    """Report whether Django can reach its database."""
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()
    except DatabaseError:
        return JsonResponse({'status': 'unhealthy'}, status=503)
    return JsonResponse({'status': 'ok'})
