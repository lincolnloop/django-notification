from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model
from django.dispatch.dispatcher import WEAKREF_TYPES


def get_receivers():
    from notification.signals import notify_user
    receivers = []
    for receiver_bits in notify_user.receivers:
        receiver = receiver_bits[1]
        if isinstance(receiver, WEAKREF_TYPES):
            receiver = receiver()
        if receiver:
            receivers.append(receiver)
    return receivers


def get_mediums():
    mediums = []
    for receiver in get_receivers():
        if hasattr(receiver, 'medium'):
            mediums.append((receiver.medium[0], receiver.medium[1]))
    return tuple(mediums)


def get_medium_default(medium):
    for receiver in get_receivers():
        if hasattr(receiver, 'medium'):
            if int(receiver.medium[0]) == int(medium):
                return receiver.medium[2]


def get_notification_language(user):
    """
    Returns site-specific notification language for this user. Raises
    LanguageStoreNotAvailable if this site does not use translated
    notifications.
    """
    if getattr(settings, 'NOTIFICATION_LANGUAGE_MODULE', False):
        try:
            app_label, model_name = settings.NOTIFICATION_LANGUAGE_MODULE.split('.')
            model = get_model(app_label, model_name)
            language_model = model._default_manager.get(user__id__exact=user.id)
            if hasattr(language_model, 'language'):
                return language_model.language
        except (ImportError, ImproperlyConfigured, model.DoesNotExist):
            pass
