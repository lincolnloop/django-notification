from django.conf import settings

LANGUAGE_MODULE = getattr(settings, 'NOTIFICATION_LANGUAGE_MODULE', None)

BACKENDS = getattr(settings, 'NOTIFICATION_BACKENDS',
                   ('notification.backends.ModelBackend',
                    'notification.backends.EmailBackend'))

# lock timeout value. how long to wait for the lock to become available.
# default behavior is to never wait for the lock to be available.
LOCK_WAIT_TIMEOUT = getattr(settings, "NOTIFICATION_LOCK_WAIT_TIMEOUT", -1)

QUEUE_ALL = getattr(settings, "NOTIFICATION_QUEUE_ALL", False)
