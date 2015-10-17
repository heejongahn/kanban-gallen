#!/usr/bin/env python
# vim: fileencoding=utf-8 tabstop=2 softtabstop=2 shiftwidth=2 expandtab

import datetime

from sqlalchemy.dialects import mysql
from kanban_gallen import db


def UnicodeString(n):
  return db.Unicode(n).with_variant(
    mysql.VARCHAR(n, collation='utf8_bin'), 'mysql')


def Text():
  return db.Text().with_variant(mysql.TEXT(collation='utf8_bin'), 'mysql')


class KanbanColumn(db.Model):
  __tablename__ = 'kanban_column'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(UnicodeString(256), nullable=False)
  portlets = db.relationship("KanbanPortlet", backref="kanban_portlet",
                             cascade="all, delete-orphan")

  def __init__(self, title):
    self.title = title


class KanbanPortlet(db.Model):
  __tablename__ = 'kanban_portlet'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(UnicodeString(256), nullable=False)
  content = db.Column(Text(), nullable=True)
  tag = db.Column(UnicodeString(256), nullable=True)
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

  def to_dict(self):
    return {
      'id': self.id,
      'title': self.title,
      'content': self.content,
      'tag': self.tag,
      'created': self.created,
      'modified': self.modified,
      'archived': self.archived
    }
