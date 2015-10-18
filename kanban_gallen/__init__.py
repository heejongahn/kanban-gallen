#!/usr/bin/env python
# vim: fileencoding=utf-8 tabstop=2 softtabstop=2 shiftwidth=2 expandtab
""" __init__.py """

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('kanban_gallen.settings')

if 'KANBAN_GALLEN' in os.environ:
  app.config.from_envvar('KANBAN_GALLEN')

db = SQLAlchemy(app)


from kanban_gallen import models, views
