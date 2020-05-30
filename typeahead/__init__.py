import os
from flask import Flask


app = Flask(__name__)
# Load Config
if os.environ.get('TYPEAHEAD_SETTINGS'):
    app.config.from_envvar('TYPEAHEAD_SETTINGS')
else:
    # use default
    path = os.path.dirname(__file__)
    path = os.path.join(path, 'config.py')
    if os.path.isfile(path):
        app.config.from_object('typeahead.config.DevelopmentConfig')
    else:
        print('PLEASE SET A CONFIG FILE WITH TYPEAHEAD_SETTINGS OR '
              'PUT ONE AT typeahead/config.py')
        exit(-1)

with app.app_context():
    from . import commands
