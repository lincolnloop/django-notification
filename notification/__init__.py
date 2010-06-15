VERSION = (0, 2, 0, "dev", 2)

def get_version():
    if VERSION[3] == "final":
        return "%s.%s.%s" % (VERSION[0], VERSION[1], VERSION[2])
    elif VERSION[3] == "dev":
        return "%s.%s.%s.%s%s" % (VERSION[0], VERSION[1], VERSION[2], VERSION[3], VERSION[4])
    else:
        return "%s.%s.%s%s" % (VERSION[0], VERSION[1], VERSION[2], VERSION[3])

__version__ = get_version()

def register_backend():
    """
    Register the mail backend.
    """
    from notification import backends, signals
    signals.notify_user.connect(backends.send_email)

register_backend()
