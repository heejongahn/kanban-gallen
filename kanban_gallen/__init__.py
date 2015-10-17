#!/usr/bin/env python
# vim: fileencoding=utf-8 tabstop=2 softtabstop=2 shiftwidth=2 expandtab

import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('kanban_gallen.settings')

if os.environ.has_key('KANBAN_GALLEN'):
  app.config.fron_envvar('KANBAN_GALLEN')

db = SQLAlchemy(app)


from kanban_gallen import models, views
