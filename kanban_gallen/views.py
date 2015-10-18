#!/usr/bin/env python
# vim: fileencoding=utf-8 tabstop=2 softtabstop=2 shiftwidth=2 expandtab

import datetime
import httplib
import json

from flask import abort, render_template, request
from sqlalchemy.exc import IntegrityError

from kanban_gallen import app, db
from .models import KanbanColumn, KanbanPortlet


def create_column_result(success, id=None, title=None):
  return json.dumps({'success': success, 'id': id, 'title': title})


def create_portlet_result(success, id=None, title=None, content=None):
  return json.dumps({'success': success, 'id': id, 'title': title,
                    'content': content})


@app.route('/', methods=['GET'])
def index():
  columns = KanbanColumn.query.all()
  return render_template('index.html', columns=columns)


@app.route('/create/column', methods=['POST'])
@app.route('/create/column/', methods=['POST'])
def create_column():
  new_title = 'New Column'
  column = KanbanColumn(new_title)

  try:
    db.session.add(column)
    db.session.commit()
  except IntegrityError:
    abort(httplib.BAD_REQUEST, 'BAD REQUEST')
    return create_column_result(False)
  return create_column_result(True, column.id, column.title)


@app.route('/create/portlet/<column_id>', methods=['POST'])
@app.route('/create/portlet/<column_id>/', methods=['POST'])
def create_portlet(column_id):
  column = KanbanColumn.query.get(column_id)

  if not column:
    abort(httplib.NOT_FOUND, 'COLUMN NOT FOUND')

  new_title = "New Portlet"
  new_content = "click to edit..."
  portlet = KanbanPortlet(new_title, new_content)
  try:
    column.portlets.append(portlet)
    db.session.add(portlet)
    db.session.commit()
  except IntegrityError:
    abort(httplib.BAD_REQUEST, 'BAD REQUEST')
    return create_portlet_result(False)
  return create_portlet_result(True, portlet.id, portlet.title,
                               portlet.content)


@app.route('/edit/portlet/<portlet_id>', methods=['PUT'])
@app.route('/edit/portlet/<portlet_id>/', methods=['PUT'])
def edit_portlet(portlet_id):
  portlet = KanbanPortlet.query.get(portlet_id)

  portlet.modified = datetime.datetime.utcnow()
  if 'title' in request.values:
    portlet.title = request.values['title']
  elif 'content' in request.values:
    portlet.content = request.values['content']
  elif 'column_id' in request.values:
    portlet.column_id = request.values['column_id']

  try:
    db.session.commit()
  except IntegrityError:
    abort(httplib.BAD_REQUEST, 'BAD REQUEST')
  return create_portlet_result(True, portlet.id, portlet.title,
                               portlet.content)


@app.route('/delete/column/<column_id>', methods=['DELETE'])
@app.route('/delete/column/<column_id>/', methods=['DELETE'])
def delete_column(column_id):
  column = KanbanColumn.query.get(column_id)

  if not column:
    abort(httplib.NOT_FOUND, 'COLUMN NOT FOUND')

  try:
    db.session.delete(column)
    db.session.commit()
  except IntegrityError:
    abort(httplib.BAD_REQUEST, 'BAD REQUEST')

  msg = "Deleted Column: {0}.".format(column_id)
  return json.dumps({'success': True, 'msg': msg})


@app.route('/delete/portlet/<portlet_id>', methods=['DELETE'])
@app.route('/delete/portlet/<portlet_id>/', methods=['DELETE'])
def delete_portlet(portlet_id):
  portlet = KanbanPortlet.query.get(portlet_id)

  if not portlet:
    abort(httplib.NOT_FOUND, 'PORTLET NOT FOUND')

  try:
    db.session.delete(portlet)
    db.session.commit()
  except IntegrityError:
    abort(httplib.BAD_REQUEST, 'BAD REQUEST')

  msg = "Deleted Card: {0}.".format(portlet_id)
  return json.dumps({'success': True, 'msg': msg})
