"""
An emailing notification backend for django-notification.
"""
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy

# favour django-mailer but fall back to django.core.mail
if 'mailer' in settings.INSTALLED_APPS:
    from mailer import send_mail
else:
    from django.core.mail import send_mail


class BaseBackend(object):
    mediums = ()

    def send(self):
        raise NotImplementedError()


class ModelBackend(BaseBackend):

    def send(self, user, notice_type, on_site, sender, context, **kwargs):
        """
        Create a Notice model.
        """
        from notification.models import Notice
        message = notice_type.render_template('notice.html', context)
        Notice.objects.create(recipient=user, message=message,
            notice_type=notice_type, on_site=on_site, sender=sender)


class EmailBackend(BaseBackend):
    mediums = (('1', ugettext_lazy('Email')),)
    medium_defaults = {'1': 2}

    def send(self, user, notice_type, context, **kwargs):
        """
        Send the notification to a user as an e-mail.
        """
        if not user.email or not notice_type.should_send(user, '1'):
            return

        # Strip newlines from subject
        subject = ''.join(render_to_string('notification/email_subject.txt', {
            'message': notice_type.render_template('short.txt', context),
        }, context).splitlines())

        body = render_to_string('notification/email_body.txt', {
            'message': notice_type.render_template('full.txt', context),
        }, context)

        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])
