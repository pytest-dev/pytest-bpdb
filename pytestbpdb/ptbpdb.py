""" interactive debugging with PDB, the Python Debugger. """
from __future__ import absolute_import
import bpdb as pdb
import sys

import pytest
import py


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group._addoption('--bpdb',
                     action="store_true", dest="usebpdb", default=False,
                     help="start the interactive Bpython debugger on errors.")


def pytest_namespace():
    return {'set_trace': pytestBPDB().set_trace}


def pytest_configure(config):
    if config.getvalue("usebpdb"):
        config.pluginmanager.register(BpdbInvoke(), 'bpdbinvoke')

    old = (pdb.set_trace, pytestBPDB._pluginmanager)

    def fin():
        pdb.set_trace, pytestBPDB._pluginmanager = old
    pdb.set_trace = pytest.set_trace
    pytestBPDB._pluginmanager = config.pluginmanager
    config._cleanup.append(fin)


class pytestBPDB:
    """ Pseudo PDB that defers to the real pdb. """
    _pluginmanager = None

    def set_trace(self):
        """ invoke PDB set_trace debugging, dropping any IO capturing. """
        frame = sys._getframe().f_back
        capman = None
        if self._pluginmanager is not None:
            capman = self._pluginmanager.getplugin("capturemanager")
            if capman:
                capman.suspendcapture(in_=True)
            tw = py.io.TerminalWriter()
            tw.line()
            tw.sep(">", "PDB set_trace (IO-capturing turned off)")
            self._pluginmanager.hook.pytest_enter_pdb()
        pdb.BPdb().set_trace(frame)


class BpdbInvoke:
    def pytest_exception_interact(self, node, call, report):
        capman = node.config.pluginmanager.getplugin("capturemanager")
        if capman:
            capman.suspendcapture(in_=True)
        _enter_pdb(node, call.excinfo, report)

    def pytest_internalerror(self, excrepr, excinfo):
        for line in str(excrepr).split("\n"):
            sys.stderr.write("INTERNALERROR> %s\n" % line)
            sys.stderr.flush()
        tb = _postmortem_traceback(excinfo)
        post_mortem(tb)


def _enter_pdb(node, excinfo, rep):
    # XXX we re-use the TerminalReporter's terminalwriter
    # because this seems to avoid some encoding related troubles
    # for not completely clear reasons.
    tw = node.config.pluginmanager.getplugin("terminalreporter")._tw
    tw.line()
    tw.sep(">", "traceback")
    rep.toterminal(tw)
    tw.sep(">", "entering PDB")
    tb = _postmortem_traceback(excinfo)
    post_mortem(tb)
    rep._pdbshown = True
    return rep


def _postmortem_traceback(excinfo):
    # A doctest.UnexpectedException is not useful for post_mortem.
    # Use the underlying exception instead:
    from doctest import UnexpectedException
    if isinstance(excinfo.value, UnexpectedException):
        return excinfo.value.exc_info[2]
    else:
        return excinfo._excinfo[2]


def _find_last_non_hidden_frame(stack):
    i = max(0, len(stack) - 1)
    while i and stack[i][0].f_locals.get("__tracebackhide__", False):
        i -= 1
    return i


def post_mortem(t):
    class BPdb(pdb.BPdb):
        def get_stack(self, f, t):
            stack, i = pdb.BPdb.get_stack(self, f, t)
            if f is None:
                i = _find_last_non_hidden_frame(stack)
            return stack, i
    p = BPdb()
    p.reset()
    p.interaction(None, t)
