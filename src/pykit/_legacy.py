"""
Registers deprecated camelCase aliases for the pre-2027 PyKit 1.0.x API.

Imported by ``pykit/__init__.py`` so the aliases exist whichever submodule is imported first.
Each alias forwards to the snake_case name and emits a ``DeprecationWarning``.

Not aliased (internal state that was renamed): ``Logger.dataRecievers``,
``AlertLogger.errorSubscribers``/``warningSubscribers``/``infoSubscribers``,
``LogTable._timestamp``, and ``LoggedPowerDistribution(moduleId=..., moduleType=...)`` keyword names.
"""

from pykit._compat import add_aliases, deprecated_property
from pykit.alertlogger import AlertLogger
from pykit.inputs.loggableds import LoggedDriverStation
from pykit.inputs.loggablepowerdistribution import LoggedPowerDistribution
from pykit.inputs.loggablesystemstats import LoggedSystemStats
from pykit.loggedrobot import LoggedRobot
from pykit.logger import Logger
from pykit.logtable import LogTable
from pykit.networktables.loggeddashboardchooser import LoggedDashboardChooser
from pykit.networktables.loggednetworkinput import LoggedNetworkInput
from pykit.networktables.loggednetworkvalue import LoggedNetworkValue
from pykit.networktables.nt4Publisher import NT4Publisher
from pykit.wpilog.wpilogwriter import WPILOGWriter
from pykit.logdatareceiver import LogDataReceiver

_ALIASES: dict[type, dict[str, str]] = {
    Logger: {"startReciever": "start_receiver"},
    AlertLogger: {"registerGroup": "register_group"},
    LoggedDriverStation: {
        "saveToTable": "save_to_table",
        "loadFromTable": "load_from_table",
    },
    LoggedPowerDistribution: {
        "getInstance": "get_instance",
        "saveToTable": "save_to_table",
    },
    LoggedSystemStats: {"saveToTable": "save_to_table"},
    LogTable: {
        "addStructSchema": "add_struct_schema",
        "addStructSchemaNest": "add_struct_schema_nest",
        "getAll": "get_all",
        "getRaw": "get_raw",
        "getBoolean": "get_boolean",
        "getInteger": "get_integer",
        "getFloat": "get_float",
        "getDouble": "get_double",
        "getString": "get_string",
        "getBooleanArray": "get_boolean_array",
        "getIntegerArray": "get_integer_array",
        "getFloatArray": "get_float_array",
        "getDoubleArray": "get_double_array",
        "getStringArray": "get_string_array",
        "putValue": "put_value",
        "writeAllowed": "write_allowed",
    },
    LoggedDashboardChooser: {
        "getSelected": "get_selected",
        "onChange": "on_change",
        "toLog": "to_log",
        "fromLog": "from_log",
    },
    LoggedNetworkInput: {"removeSlash": "remove_slash"},
    LoggedNetworkValue: {
        "setDefault": "set_default",
        "toLog": "to_log",
        "fromLog": "from_log",
    },
    LogDataReceiver: {"putTable": "put_table"},
    NT4Publisher: {"putTable": "put_table"},
    WPILOGWriter: {"putTable": "put_table"},
}

for _cls, _mapping in _ALIASES.items():
    add_aliases(_cls, _mapping)

LoggedRobot.useTiming = deprecated_property("useTiming", "use_timing")
LoggedRobot.initEnd = deprecated_property("initEnd", "init_end")
LoggedPowerDistribution.moduleId = deprecated_property("moduleId", "module_id")
LoggedPowerDistribution.moduleType = deprecated_property("moduleType", "module_type")
