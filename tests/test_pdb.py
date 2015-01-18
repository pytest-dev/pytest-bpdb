# -*- coding: utf-8 -*-

pytest_plugins = "pytester"


class Option(object):
    def __init__(self, no_bpdb=False):
        self.no_bpdb = no_bpdb

    @property
    def args(self):
        if self.no_bpdb:
            l = ['--pdb']
        else:
            l = ['--bpdb']
        return l


def pytest_generate_tests(metafunc):
    if "option" in metafunc.fixturenames:
        metafunc.addcall(id="default",
                         funcargs={'option': Option(no_bpdb=False)})
        metafunc.addcall(id="no_bpdb",
                         funcargs={'option': Option(no_bpdb=True)})


def test_post_mortem(testdir, option):
    testdir.makepyfile(
        """
        def test_func():
            assert 0
        """
    )

    result = testdir.runpytest(*option.args)

    if option.no_bpdb:
        result.stdout.fnmatch_lines(['(Pdb) '])
    else:
        result.stdout.fnmatch_lines([
            'Use "B" to enter bpython, Ctrl-d to exit it.',
            '(BPdb) '
        ])


def test_pytest_set_trace(testdir, option):
    testdir.makepyfile(
        """
        import pytest

        def test_func():
            pytest.set_trace()
        """
    )

    result = testdir.runpytest(*option.args)

    result.stdout.fnmatch_lines([
        'Use "B" to enter bpython, Ctrl-d to exit it.',
        '(BPdb) ',
    ])


def test_bpdb_set_trace(testdir, option):
    testdir.makepyfile(
        """
        import bpdb

        def test_func():
            bpdb.set_trace()
        """
    )

    result = testdir.runpytest(*option.args)

    result.stdout.fnmatch_lines([
        'Use "B" to enter bpython, Ctrl-d to exit it.',
        '(BPdb) ',
    ])
