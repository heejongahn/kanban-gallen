#!/usr/bin/env python
# vim: fileencoding=utf-8 tabstop=2 softtabstop=2 shiftwidth=2 expandtab

from flask import render_template

from kanban_gallen import app


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
