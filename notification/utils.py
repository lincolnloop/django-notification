from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model
from django.dispatch.dispatcher import WEAKREF_TYPES
from django.utils.importlib import import_module

from notification import settings


def get_backends():
    for module in settings.BACKENDS:
        yield import_module(module)()


def get_mediums():
    mediums = []
    for backend in get_backends():
        backend_mediums = getattr(backend, 'mediums', None)
        if backend_mediums:
            mediums.extend(backend_mediums)
    return tuple(mediums)


def get_medium_default(medium):
    for backend in get_backends():
        defaults = getattr(backend, 'medium_defaults', None) or {}
        default = defaults.get(medium)
        if default is not None:
            return default


def get_notification_language(user):
    """
    Returns site-specific notification language for this user. Raises
    LanguageStoreNotAvailable if this site does not use translated
    notifications.
    """
    if settings.LANGUAGE_MODULE:
        try:
            app_label, model_name = settings.LANGUAGE_MODULE.split('.')
            model = get_model(app_label, model_name)
            language_model = model._default_manager.get(user__id__exact=user.id)
            if hasattr(language_model, 'language'):
                return language_model.language
        except (ImportError, ImproperlyConfigured, model.DoesNotExist):
            pass
