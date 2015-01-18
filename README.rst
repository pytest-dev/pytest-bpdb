===========
pytest-bpdb
===========

A pytest_ plugin for dropping to bpdb_ on test failures.

.. _pytest: http://pytest.org
.. _bpdb: http://docs.bpython-interpreter.org/bpdb.html

.. image:: https://travis-ci.org/slafs/pytest-bpdb.png?branch=master
        :target: https://travis-ci.org/slafs/pytest-bpdb

.. image:: https://badge.fury.io/py/pytest-bpdb.png
    :target: http://badge.fury.io/py/pytest-bpdb

.. image:: https://pypip.in/d/pytest-bpdb/badge.png
        :target: https://pypi.python.org/pypi/pytest-bpdb

This plugin is almost entirely based on built-in `pytest pdb plugin`_
and `pytest-ipdb`_ plugin

.. _pytest pdb plugin: https://bitbucket.org/hpk42/pytest/src/d942d16857f3fd225d25bc21aa6531449163528c/_pytest/pdb.py?at=default
.. _pytest-ipdb: https://github.com/mverteuil/pytest-ipdb

Installation
============

To install the plugin run::

    pip install pytest-bpdb

or use a development version::

    pip install -e git+git://github.com/slafs/pytest-bpdb


Usage
=====

To enable a BPython debugger (bpdb) on pytest failures use a ``--bpdb`` option.
For example::

    py.test --bpdb tests/
