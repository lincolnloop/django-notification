from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model
from django.utils.importlib import import_module

from notification import settings

_backends = []


def get_backends():
    if _backends:
        return _backends
    for path in settings.BACKENDS:
        module, attr = path.rsplit('.', 1)
        try:
            mod = import_module(module)
        except ImportError, e:
            raise ImproperlyConfigured('Error importing notification backend '
                                       '%s: "%s"' % (module, e))
        try:
            cls = getattr(mod, attr)
        except AttributeError:
            raise ImproperlyConfigured('Module "%s" does not define a "%s" '
                                       'notification backend' % (module, attr))
        _backends.append(cls())
    return _backends


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
            language_model = model._default_manager.get(
                user__id__exact=user.id)
            if hasattr(language_model, 'language'):
                return language_model.language
        except (ImportError, ImproperlyConfigured, model.DoesNotExist):
            pass
