from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.template.loader import get_template

import smtplib
import os


def send_email(request=None, data=None):
    msg = MIMEMultipart()
    context = dict()

    # create message
    msg['From'] = data['sender']
    msg['To'] = data['recipient']
    msg['Subject'] = data['subject']

    # set context
    context['type'] = data['type']
    context['content'] = data['content']
    context['payload'] = data['payload']

    # create body
    body = html_renderer(request, context)

    msg.attach(MIMEText(body, 'html'))

    # create server
    server = smtplib.SMTP(os.environ['EMAIL_HOST'], os.environ['EMAIL_PORT'])
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(os.environ['EMAIL_HOST_USER'], os.environ['EMAIL_HOST_USER_PASSWORD'])
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()


def html_renderer(request=None, context=None):
    template = get_template('email_template.html')
    return template.render(context, request)
