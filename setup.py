#!/usr/bin/env python
# vim: fileencoding=utf-8 tabstop=2 softtabstop=2 shiftwidth=2 expandtab


from setuptools import setup, find_packages


setup(
  name='kanban_gallen',
  version=open('VERSION').read().strip(),
  author='gallen',
  author_email='seirios0107@gmail.com',
  license='BSD',
  url='gallen.in',
  keywords='flask',
  description=('My coding test app.'),
  long_description=('My coding test app: the minimal kanban board.'),
  packages=find_packages(),
  zip_safe=False,
)
