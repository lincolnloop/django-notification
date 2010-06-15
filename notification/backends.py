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

MAIL_BACKEND_ID = '1'


def send_email(sender, user, notice_type, context, **kwargs):
    """
    Send the notification to a user as an e-mail.
    """
    if not user.email or not notice_type.should_send(user, MAIL_BACKEND_ID):
        return

    # Strip newlines from subject
    subject = ''.join(render_to_string('notification/email_subject.txt', {
        'message': notice_type.render_template('short.txt', context),
    }, context).splitlines())

    body = render_to_string('notification/email_body.txt', {
        'message': notice_type.render_template('full.txt', context),
    }, context)

    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])

send_email.medium = (MAIL_BACKEND_ID, ugettext_lazy('Email'), 2)
