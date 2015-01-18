===========
pytest-bpdb
===========

A pytest_ plugin for dropping to bpdb_ on test failures.

.. _pytest: http://pytest.org
.. _bpdb: http://docs.bpython-interpreter.org/bpdb.html

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
