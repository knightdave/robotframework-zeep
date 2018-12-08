#!/usr/bin/env python

from os.path import abspath, dirname, join

try:
    from setuptools import setup
except ImportError as error:
    from distutils.core import setup

CURDIR = dirname(abspath(__file__))

with open(join(CURDIR, 'src', 'ZeepLibrary', 'version.py')) as f:
    exec(f.read())
    VERSION = get_version()


DESCRIPTION = """
Web service testing library for Robot Framework with modern SOAP client.
"""[1:-1]


CLASSIFIERS = """
Development Status :: 2 - Pre-Alpha
License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]

setup(name='robotframework-zeep',
      version=VERSION,
      description='Web service testing library for Robot Framework',
      long_description=DESCRIPTION,
      author='Dawid Rycerz',
      author_email='kontakt@dawidrycerz.pl',
      url='https://github.com/knightdave/robotframework-zeep',
      license='GPLv3+',
      keywords='robotframework testing test automation soap client zeep suds',
      platforms='any',
      classifiers=CLASSIFIERS.splitlines(),
      package_dir={'': 'src'},
      packages=['ZeepLibrary'],
      package_data={'ZeepLibrary': ['tests/*.robot']},
      install_requires=[
          'robotframework',
          'zeep'
      ],
      )

""" From now on use this approach
python setup.py sdist upload
git tag -a 1.2.3 -m 'version 1.2.3'
git push --tags"""
