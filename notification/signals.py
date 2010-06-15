from django.core.signals import Signal

notify_user = Signal(providing_args=['user', 'notice_type', 'context'])