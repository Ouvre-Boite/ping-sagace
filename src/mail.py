import smtplib
import ssl
import json
import os
from email.mime.text import MIMEText

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
MAIL_CONFIG_PATH = os.path.join(ROOT_DIR, 'mail_config.json')

def send_mail(subject, message):
    with open(MAIL_CONFIG_PATH, 'r') as f:
        mail_config = json.loads(f.read())

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = mail_config['sender']
    msg['To'] = mail_config['recipients']

    smtp_server = smtplib.SMTP(host=mail_config['host'], port=mail_config['port'])
    context = ssl.create_default_context()    

    result = smtp_server.starttls(context=context)
    assert result[0] == 220

    result = smtp_server.login(mail_config['user'], mail_config['password'])
    assert result[0] == 235

    result = smtp_server.send_message(msg)
    assert result == {}

    result = smtp_server.quit()
    assert result[0] == 221
