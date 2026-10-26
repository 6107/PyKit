"""Deprecated module name (misspelled). Use :mod:`pykit.logdatareceiver` instead."""

import warnings

from pykit.logdatareceiver import LogDataReceiver

warnings.warn(
    "'pykit.logdatareciever' is deprecated, use 'pykit.logdatareceiver' instead",
    DeprecationWarning,
    stacklevel=2,
)

LogDataReciever = LogDataReceiver

__all__ = ["LogDataReciever"]
