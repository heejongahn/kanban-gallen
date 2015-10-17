#!/usr/bin/env python
# vim: fileencoding=utf-8 tabstop=2 softtabstop=2 shiftwidth=2 expandtab

from flask import render_template

from kanban_gallen import app
from .models import KanbanColumn


@app.route('/', methods=['GET'])
def index():
  columns = KanbanColumn.query.all()
  return render_template('index.html', columns=columns)
