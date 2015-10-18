#!/usr/bin/env python
# vim: fileencoding=utf-8 tabstop=2 softtabstop=2 shiftwidth=2 expandtab
""" models.py """

import datetime

from sqlalchemy.dialects import mysql
from kanban_gallen import db


def unicode_string(num):
  """ utf8 받도록 설정 """
  return db.Unicode(num).with_variant(
      mysql.VARCHAR(num, collation='utf8_bin'), 'mysql')


def utf8_text():
  """ utf8 받도록 설정 """
  return db.Text().with_variant(mysql.TEXT(collation='utf8_bin'), 'mysql')


class KanbanColumn(db.Model):
  """ column에 대한 model """
  __tablename__ = 'kanban_column'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(unicode_string(256), nullable=False)
  portlets = db.relationship("KanbanPortlet", backref="kanban_portlet",
                             cascade="all, delete-orphan")

  def __init__(self, title):
    self.title = title


class KanbanPortlet(db.Model):
  """ portlet에 대한 model """
  __tablename__ = 'kanban_portlet'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(unicode_string(256), nullable=False)
  content = db.Column(utf8_text(), nullable=True)
  tag = db.Column(unicode_string(256), nullable=True)
  created = db.Column(db.DateTime(), nullable=False)
  modified = db.Column(db.DateTime(), nullable=True)
  archived = db.Column(db.Boolean(), nullable=False, default=False)
  column_id = db.Column(db.Integer, db.ForeignKey('kanban_column.id'))

  def __init__(self, title, content=None, tag=None):
    self.title = title
    self.content = content
    self.tag = tag
    self.created = datetime.datetime.utcnow()
    self.modified = None
