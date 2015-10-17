#!/usr/bin/env python
# vim: fileencoding=utf-8 tabstop=2 softtabstop=2 shiftwidth=2 expandtab

import httplib
import json

from flask import abort, render_template
from sqlalchemy.exc import IntegrityError

from kanban_gallen import app, db
from .models import KanbanColumn


@app.route('/', methods=['GET'])
def index():
  columns = KanbanColumn.query.all()
  return render_template('index.html', columns=columns)


@app.route('/create/column', methods=['POST'])
@app.route('/create/column/', methods=['POST'])
def create_column():
  column = KanbanColumn('New Column')
  try:
    db.session.add(column)
    db.session.commit()
  except IntegrityError:
    abort(httplib.BAD_REQUEST, 'BAD REQUEST')
    return json.dumps({'success': False, 'id': None})
  return json.dumps({'success': True, 'id': column.id})
