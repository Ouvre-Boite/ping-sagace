import os
import difflib
import json

import mail
import sagace

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def ping():
    credentials_path = os.path.join(ROOT_DIR, 'credentials.json')

    with open(credentials_path, 'r') as f:
        credentials = json.loads(f.read())

    for lawsuit_credentials in credentials['lawsuits']:
        process_lawsuit(
            court_id=lawsuit_credentials['court_id'],
            lawsuit_id=lawsuit_credentials['lawsuit_id'],
            lawsuit_label=lawsuit_credentials['lawsuit_label'],
            lawsuit_password=lawsuit_credentials['lawsuit_password'],
        )

def process_lawsuit(court_id, lawsuit_id, lawsuit_label, lawsuit_password):
    new_text = sagace.get_text_for_lawsuit(
        court_id=court_id,
        lawsuit_id=lawsuit_id,
        lawsuit_password=lawsuit_password,
    )

    file_path = os.path.join(
        ROOT_DIR,
        'data',
        '{}-{}.txt'.format(court_id, lawsuit_id),
    )

    try:
        with open(file_path, 'r') as f:
            old_text = f.read()

    except FileNotFoundError:
        notify_new(
            lawsuit_label=lawsuit_label,
            text=new_text,
        )
        with open(file_path, 'w') as f:
            f.write(new_text)
        return

    if new_text != old_text:
        notify_change(
            lawsuit_label=lawsuit_label,
            old_text=old_text,
            new_text=new_text,
        )
        with open(file_path, 'w') as f:
            f.write(new_text)

def compute_diff(old_text, new_text):
    diff = difflib.unified_diff(
        old_text.split('\n'),
        new_text.split('\n'),
        fromfile='old',
        tofile='new',
        lineterm='',
    )
    return '\n'.join(diff)

def notify_change(lawsuit_label, old_text, new_text):
    mail.send_mail(
        subject='Lawsuit "{}" has been updated'.format(lawsuit_label),
        message=compute_diff(old_text, new_text),
    )
    
def notify_new(lawsuit_label, text):
    mail.send_mail(
        subject='New lawsuit "{}"'.format(lawsuit_label),
        message=text,
    )
