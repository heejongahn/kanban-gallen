#!/usr/bin/env python
# vim: fileencoding=utf-8 tabstop=2 softtabstop=2 shiftwidth=2 expandtab

import os

from kanban_gallen import app, db


def create_if_not_exists(path):
  if not os.path.exists(path):
    os.mkdir(path)


if __name__ == '__main__':
  db.create_all()
  app.run(host='0.0.0.0', debug=True)
