# This file contains python variables that configure Lamson for email processing.
import logging
import os
from lamson import confirm

os.environ['DJANGO_SETTINGS_MODULE'] = 'discourse.settings'

# You may add additional parameters such as `username' and `password' if your
# relay server requires authentication, `starttls' (boolean) or `ssl' (boolean)
# for secure connections.
relay_config = {'host': 'localhost', 'port': 8825}

receiver_config = {'host': 'localhost', 'port': 8823}

handlers = ['app.handlers.bounce', 'app.handlers.admin']

slug_re = r'[-\w]+' # letters, numbers and underscores but don't start with an underscore
router_defaults = {'host': r'localhost', #TODO: CHANGEME AT DEPLOYMENT
                   'group_name': slug_re,
                   'topic': slug_re, # event or talk
                   'id_number': '[a-z0-9]+',
}

template_config = {'dir': 'app', 'module': 'templates'}

# the config/boot.py will turn these values into variables set in settings

PENDING_QUEUE = "run/pending"
ARCHIVE_BASE = "run/archive"
BOUNCE_ARCHIVE = "run/bounces"

SPAM = {'db': 'run/spamdb', 'rc': 'run/spamrc', 'queue': 'run/spam'}

from app.model.confirmation import DjangoConfirmStorage
CONFIRM = confirm.ConfirmationEngine(PENDING_QUEUE, DjangoConfirmStorage())
