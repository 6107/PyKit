"""
Backward-compatibility helpers for the pre-2027 (upstream PyKit 1.0.x) camelCase API.

The 2027 API uses snake_case names and corrected spelling (``Reciever`` -> ``Receiver``). The
helpers here keep code written against the old names working:

- ``add_aliases`` installs deprecated forwarding methods (old name -> new name) on a class.
- ``resolve_hook`` finds a user-implemented hook (such as ``to_log`` / ``toLog``) on an object
  that may have been written against either API.

Every use of an old name emits a ``DeprecationWarning``.
"""

from __future__ import annotations

import inspect
import warnings
from collections.abc import Callable
from typing import Any


def warn_deprecated(old: str, new: str, stacklevel: int = 3) -> None:
    """Emit a ``DeprecationWarning`` pointing callers from ``old`` to ``new``.

    Args:
        old: The deprecated name.
        new: The replacement name.
        stacklevel: Stack level used for the warning location.
    """
    warnings.warn(
        f"'{old}' is deprecated, use '{new}' instead",
        DeprecationWarning,
        stacklevel=stacklevel,
    )


def _make_alias(cls: type, old: str, new: str) -> Any:
    raw = inspect.getattr_static(cls, new)

    if isinstance(raw, classmethod):

        def class_alias(klass: type, *args: Any, **kwargs: Any) -> Any:
            warn_deprecated(old, new)
            return getattr(klass, new)(*args, **kwargs)

        class_alias.__name__ = old
        return classmethod(class_alias)

    if isinstance(raw, staticmethod):

        def static_alias(*args: Any, **kwargs: Any) -> Any:
            warn_deprecated(old, new)
            return getattr(cls, new)(*args, **kwargs)

        static_alias.__name__ = old
        return staticmethod(static_alias)

    def alias(self: Any, *args: Any, **kwargs: Any) -> Any:
        warn_deprecated(old, new)
        return getattr(self, new)(*args, **kwargs)

    alias.__name__ = old
    return alias


def add_aliases(cls: type, mapping: dict[str, str]) -> type:
    """Install deprecated forwarding aliases on a class.

    Args:
        cls: The class to modify.
        mapping: Maps each deprecated (old) name to the current (new) name.

    Returns:
        The same class, to allow use as a decorator helper.
    """
    for old, new in mapping.items():
        if old not in cls.__dict__:
            setattr(cls, old, _make_alias(cls, old, new))
    return cls


def deprecated_property(old: str, new: str) -> property:
    """Build a property that forwards an old attribute name to a new one.

    Args:
        old: The deprecated attribute name.
        new: The replacement attribute name.

    Returns:
        A property that warns and forwards reads and writes.
    """

    def getter(self: Any) -> Any:
        warn_deprecated(old, new)
        return getattr(self, new)

    def setter(self: Any, value: Any) -> None:
        warn_deprecated(old, new)
        setattr(self, new, value)

    return property(getter, setter)


def resolve_hook(obj: Any, new: str, old: str) -> Callable[..., Any] | None:
    """Find a hook method on an object that may implement the old or new name.

    The new name wins when both exist.

    Args:
        obj: The object to inspect.
        new: Current hook name (for example ``to_log``).
        old: Deprecated hook name (for example ``toLog``).

    Returns:
        The bound hook, or ``None`` if the object implements neither name.
    """
    hook = getattr(obj, new, None)
    if callable(hook):
        return hook
    hook = getattr(obj, old, None)
    if callable(hook):
        warn_deprecated(old, new, stacklevel=4)
        return hook
    return None
