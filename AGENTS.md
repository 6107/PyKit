# AGENTS.md – Guide for AI Coding Agents

This document describes how to work on **pykit-6107** (PyPI name `robotpy-pykit`, import name `pykit`), Team
6107's fork of the Westwood Robotics PyKit project: a pure-Python logging, telemetry, and replay framework
for FRC robots (the Python counterpart of AdvantageKit).

## Project Overview

- Python **3.14+**, built with `uv_build`, dependencies managed with `uv` (`pyproject.toml`, `uv.lock`).
- Source in `src/pykit/`, tests in `tests/`, Sphinx docs in `docs/`, sample robots in `template_projects/`.
- Depends on the 2026+ RobotPy stack (`wpilib`, `pyntcore`, `robotpy-wpimath`, `robotpy-hal`, ...).
  `robotpy-commands-v2` is only needed for `LoggedNetworkButton` (the `commands` extra / dev group).

## Relationship to lib_6107 (IMPORTANT)

Most development happens **first** in the sibling project `../lib_6107` (GitHub: `6107/frclib-6107`),
under `src/lib_6107/pykit/`. This repo is periodically synchronized from that directory.

When porting changes from lib_6107:

1. Copy the changed modules from `../lib_6107/src/lib_6107/pykit/` into `src/pykit/`.
2. **Rewrite imports**: `lib_6107.pykit.*` → `pykit.*` (the package is `pykit` here, not `lib_6107.pykit`).
3. **Preserve files that only exist here**: `src/pykit/_compat.py`, `src/pykit/_legacy.py`,
   `src/pykit/logdatareciever.py` (the backward-compatibility shim, see below). Also keep the shim hooks
   in `logger.py` (e.g. `from pykit._compat import resolve_hook`) when merging — a naive overwrite
   will drop them.
4. Port the matching tests from `../lib_6107/tests/pykit/` into `tests/` (also rewriting imports).
5. Run the test suite (below) before committing.

Do not make bug fixes only here if they belong upstream in lib_6107 — prefer fixing there first, then port,
so the two copies do not diverge. lib_6107 also has docs tracking AdvantageKit/Westwood PyKit changes
(`../lib_6107/docs/pykit-akit`).

## Directory Structure

```
pykit-6107/
├── src/pykit/
│   ├── logger.py            # Logger singleton – telemetry pipeline entry point
│   ├── loggedrobot.py       # LoggedRobot base class (replaces TimedRobot loop)
│   ├── logtable.py, logvalue.py     # Data model for logged values
│   ├── logreplaysource.py, logdatareceiver.py  # Replay input / output sinks (interfaces)
│   ├── logtracer.py         # LogTracer performance profiling spans
│   ├── alertlogger.py, autolog.py   # Alerts, @autolog input/output decorators
│   ├── LoggedMechanism*.py, LoggedNetworkButton.py
│   ├── inputs/              # Loggable wrappers (DriverStation, PowerDistribution, SystemStats)
│   ├── networktables/       # NT4Publisher and LoggedNetwork*/LoggedDashboardChooser inputs
│   ├── wpilog/              # WPILOG reader/writer + constants
│   ├── _compat.py, _legacy.py       # Deprecated camelCase shims (fork-only)
│   └── logdatareciever.py   # Deprecated misspelled module forwarding to logdatareceiver
├── tests/                   # pytest suite (tests/networktables/ mirrors src layout)
├── docs/                    # Sphinx docs (docs/source, `make html` in docs/)
├── template_projects/       # diff_drive, kitbot_2025, skeleton example robots
├── .github/workflows/       # Inherited from upstream PyKit; see CI note below
└── pyproject.toml, .pylintrc, .readthedocs.yaml
```

## Naming & Backward-Compatibility Shim

This fork is moving to PEP 8 naming (snake_case methods/variables, enforced with ruff/pylint). Upstream
names are kept alive via a shim:

- New code uses **snake_case**; old camelCase names (e.g. `LogTable.getInteger`, `Logger.startReciever`,
  `LoggedRobot.useTiming`) still work in `src/pykit/_legacy.py` / `_compat.py` and emit `DeprecationWarning`.
- User classes implementing old `toLog`/`fromLog`/`putTable` hooks must still be invoked
  (`resolve_hook` in `_compat.py`).
- `pykit.logdatareciever` (misspelled) forwards to `pykit.logdatareceiver`.
- Intentionally **not** aliased: `Logger.dataRecievers`, the `AlertLogger` subscriber dictionaries, and the
  `moduleId`/`moduleType` constructor keywords of `LoggedPowerDistribution`.
- When renaming a public API, add a legacy alias plus a test in `tests/test_legacy_aliases.py`.
  Never remove an old name without an explicit decision to end deprecation.
- Some module filenames (`LoggedMechanism2d.py`, `LoggedNetworkButton.py`) keep their original
  CamelCase to stay compatible with upstream and lib_6107; do not rename them casually.

## Developer Workflows

Run from the repo root.

```powershell
uv sync --group dev                 # create .venv and install deps (add --extra commands if needed)
uv run python -m pytest             # run tests (pythonpath=src, testpaths=tests)
uv run python -m pytest --cov=pykit # with coverage
uvx ruff check src tests            # lint (ruff is used for PEP 8 naming checks; not a project dependency)
uvx pylint src/pykit                # pylint, config in .pylintrc
uvx mypy src/pykit                  # optional type check, config in pyproject.toml
uv build                            # build sdist/wheel into dist/
```

- Tests must pass without a robot or simulator; they run against the RobotPy simulation HAL.
- `LoggedNetworkButton` tests need `robotpy-commands-v2` (in the dev group).
- Docs: `cd docs; make html` (Sphinx; `docs/source/pykit*.rst` are the module listings).

### Continuous Integration

The workflows in `.github/workflows/` still point at the original upstream project (1757WestwoodRobotics)
and are **to be replaced** by workflows modeled after `../lib_6107/.github/workflows/` (`ci.yml` running
pytest on ubuntu/windows, `code-quality.yml` running pre-commit/ruff). Ignore them for now: do not edit,
fix, or rely on them unless asked.

## Key Concepts

- **Logger singleton** – all telemetry flows through `Logger` (e.g. `Logger.recordOutput`; the snake_case
  rename is in progress, so check the current name in source), not `SmartDashboard`. Modes: REAL, SIM, and REPLAY (driven by a `LogReplaySource`).
- **LoggedRobot** – replaces `TimedRobot`; drives the loop, pulls inputs, writes outputs, and can run in
  replay at maximum speed with timing disabled.
- **Receivers/Sources** – `LogDataReceiver` implementations (`NT4Publisher`, `WPILOGWriter`) consume a
  `LogTable`; `WPILOGReader` is a `LogReplaySource`.
- **autolog** – `@autolog` / `@autologgable_output` / `autolog_output` decorators and `AutoLogInputManager` /
  `AutoLogOutputManager` serialize IO objects into a `LogTable`.
- **LogTracer** – span-based profiling that logs timings to the table.
- Compatibility with AdvantageKit/AdvantageScope log formats matters: avoid changing WPILOG or NT4 key
  layouts and `LogValue` type mapping without a strong reason.

## Conventions

- Follow PEP 8, with type hints where practical; match the style of surrounding code.
- Keep the library free of team-specific code — robot-specific helpers belong in lib_6107.
- Add or update tests in `tests/` for every behavior change; follow the `test_<module>.py` naming.
- Keep `README.md` in sync if you change user-facing behavior; `README_legacy.md` is the untouched upstream
  readme and should not be edited.
- Preserve license files (`LICENSE`, `AdvantageKit-License.md`, `WPILib-License.md`) and the
  `template_projects/*` license notices.
- Don't commit `.idea/`, `.venv/`, `dist/`, or coverage output.

## Troubleshooting

1. **`ModuleNotFoundError: pykit`** – run via `uv run` or ensure `src/` is on `PYTHONPATH` (pytest config
   already sets it).
2. **`ModuleNotFoundError: lib_6107.pykit...` after a port** – an import was not rewritten to `pykit.*`.
3. **`DeprecationWarning` noise in tests** – you are calling a legacy name; use the snake_case API.
4. **Replay issues** – confirm the log path and that timing is disabled (`LoggedRobot` replay mode).
