#!/usr/bin/env python
# vim: fileencoding=utf-8 tabstop=2 softtabstop=2 shiftwidth=2 expandtab
"""views.py"""

import datetime
import httplib
import json

from flask import abort, render_template, request
from sqlalchemy.exc import IntegrityError

from kanban_gallen import app, db
from .models import KanbanColumn, KanbanPortlet


def create_column_result(success, _id=None, title=None):
  """ column 생성 시 리턴할 메시지 만들어 줌 """
  return json.dumps({'success': success, 'id': _id, 'title': title})


def create_portlet_result(success, _id=None, title=None, content=None):
  """ portlet 생성 시 리턴할 메시지 만들어 줌 """
  return json.dumps({'success': success, 'id': _id, 'title': title,
                     'content': content})


@app.route('/', methods=['GET'])
def index():
  """ index 페이지 리턴 """
  columns = KanbanColumn.query.all()
  archived_portlets = KanbanPortlet.query.filter_by(archived=True).all()
  return render_template('index.html', columns=columns,
                         archived_portlets=archived_portlets)


@app.route('/archive/portlet/<element_id>', methods=['PUT'])
@app.route('/archive/portlet/<element_id>/', methods=['PUT'])
def archive_portlets(element_id):
  """ portlet 하나 혹은 한 column내의 모든 portlet 아카이브 """
  element_type = request.values['type']
  id_list = []
  # portlet 하나를 아카이브 할 때
  if element_type == "portlet":
    portlet = KanbanPortlet.query.get(element_id)
    portlet.archived = True
    id_list.append(portlet.id)

  # 한 column 내의 모든 portlet들을 아카이브 할 때
  elif element_type == "column":
    column = KanbanColumn.query.get(element_id)

    # 이미 아카이브가 된 portlet들은 제외한 portlet들을 아카이브 하기 위함
    portlets = [p for p in column.portlets if p.archived is False]

    for portlet in portlets:
      portlet.archived = True
      id_list.append(portlet.id)
  try:
    db.session.commit()
  except IntegrityError:
    abort(httplib.BAD_REQUEST, 'BAD REQUEST')
  return json.dumps({'success': True, 'id_list': id_list})


@app.route('/create/column', methods=['POST'])
@app.route('/create/column/', methods=['POST'])
def create_column():
  """ column 생성 """
  new_title = 'Column'
  column = KanbanColumn(new_title)
  try:
    db.session.add(column)
    db.session.commit()
    column.title = 'Column {0}'.format(column.id)
    db.session.commit()
  except IntegrityError:
    abort(httplib.BAD_REQUEST, 'BAD REQUEST')
    return create_column_result(False)
  return create_column_result(True, column.id, column.title)


@app.route('/create/portlet/<column_id>', methods=['POST'])
@app.route('/create/portlet/<column_id>/', methods=['POST'])
def create_portlet(column_id):
  """ portlet 생성 """
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
  """ portlet 정보 수정 """
  portlet = KanbanPortlet.query.get(portlet_id)

  portlet.modified = datetime.datetime.utcnow()
  attr = request.values['attr']
  value = request.values['value']
  if attr == 'title':
    portlet.title = value
  elif attr == 'content':
    portlet.content = value
  elif attr == 'column':
    portlet.column_id = value

  try:
    db.session.commit()
  except IntegrityError:
    abort(httplib.BAD_REQUEST, 'BAD REQUEST')
  return create_portlet_result(True, portlet.id, portlet.title,
                               portlet.content)


@app.route('/delete/column/<column_id>', methods=['DELETE'])
@app.route('/delete/column/<column_id>/', methods=['DELETE'])
def delete_column(column_id):
  """ column 삭제 """
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
  """ portlet 삭제 """
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
