"""Tests for the deprecated pre-2027 camelCase aliases."""

import importlib
import sys

import pytest

import pykit
from pykit._compat import add_aliases, resolve_hook
from pykit.logdatareceiver import LogDataReceiver
from pykit.logger import Logger
from pykit.logtable import LogTable


def test_logtable_getters_forward_and_warn():
    table = LogTable(0)
    table.put("a", 3)
    with pytest.warns(DeprecationWarning, match="get_integer"):
        assert table.getInteger("a", 0) == 3
    with pytest.warns(DeprecationWarning, match="get_boolean"):
        assert table.getBoolean("missing", True) is True


def test_classmethod_alias_forwards():
    class Sample:
        @classmethod
        def new_name(cls, value):
            return (cls, value)

    add_aliases(Sample, {"oldName": "new_name"})
    with pytest.warns(DeprecationWarning, match="new_name"):
        assert Sample.oldName(5) == (Sample, 5)


def test_resolve_hook_prefers_new_name():
    class Both:
        def put_table(self, table):
            return "new"

        def putTable(self, table):  # noqa: N802
            return "old"

    assert resolve_hook(Both(), "put_table", "putTable")(None) == "new"


def test_resolve_hook_falls_back_to_old_name_with_warning():
    class Old:
        def putTable(self, table):  # noqa: N802
            return "old"

    with pytest.warns(DeprecationWarning, match="put_table"):
        hook = resolve_hook(Old(), "put_table", "putTable")
    assert hook(None) == "old"


def test_resolve_hook_missing_returns_none():
    assert resolve_hook(object(), "put_table", "putTable") is None


def test_process_inputs_supports_legacy_inputs_class():
    class LegacyInputs:
        def toLog(self, table, prefix):  # noqa: N802
            table.put(f"{prefix}/x", 1)

        def fromLog(self, table, prefix):  # noqa: N802
            pass

    table = LogTable(0)
    saved = (Logger.running, Logger.entry)
    Logger.running, Logger.entry = True, table
    try:
        with pytest.warns(DeprecationWarning, match="to_log"):
            Logger.processInputs("/Legacy", LegacyInputs())
    finally:
        Logger.running, Logger.entry = saved
    assert table.get("/Legacy/x", 0) == 1


def test_legacy_receiver_module_alias():
    sys.modules.pop("pykit.logdatareciever", None)
    with pytest.warns(DeprecationWarning, match="logdatareceiver"):
        module = importlib.import_module("pykit.logdatareciever")
    assert module.LogDataReciever is LogDataReceiver


def test_logged_robot_use_timing_alias():
    from pykit.loggedrobot import LoggedRobot

    assert isinstance(LoggedRobot.__dict__["useTiming"], property)
    assert pykit._legacy is not None
