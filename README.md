# PyKit

This current check-in has not been tested by itself or on a robot. It has been tested in
the lib_6107 project (see below) and the changes have been ported to this project. I will
remove this note once I have tested it out under simulation on a robot...
---

Now on to the reset of the README.md file

This is a fork of the Westwood Robotics PyKit project, which is a Pure-Python logging, telemetry,
and replay framework developed by [Team 1757](https://whsrobotics.org) for use on Python robots. 
PyKit enables replaying log files to re-simulate robot code based on real data.

During the 2026 season, I ran across a few issues with the original PyKit project, and I decided 
to fork it and make some improvements and fixes and unit test coverage. Also a bit of refactoring 
to make it in line with most python coding styles.

Since the 2026 season, AdvantageKit has been updated with improvement and to prepare it for the
2027 season and the changes to the wpilib and/or controller (SystemCore).  The Westwood 
PyKit project has not been updated since 2026, and I have decided to continue to maintain this 
fork of the project.

## lib_6107
When I did the original fork, I decided for 2027 to create a base python library to help with
some of the common tasks and objects and it is named [lib_6107](https://github.com/6107/frclib-6107).
most all of my debug on pykit for 2027 will be made there first and ported to this project as needed
and when time allows.  So take a look at that projects .../src/lib_6107/pykit subdirectory
for any latest changes.

## Tracking AdvantageKit
In the [lib_6107 docs](https://github.com/6107/frclib-6107/docs/pykit-akit) subirectory, there
are some markdown documents I had github copilot generate to help track changes in AdvantageKit
and WestWood's PyKit project.  They may be of interest to you if you are trying to track changes
in those projects.  

I will try to keep these up to date (perhaps every 3-5 weeks) until build season comes. I think build
season will be pretty busy with SystemCore challenges, so analysis of advantageKit will increase
in frequence for a while, but updates to this project will be less frequent

## Class, Function, and Variable Naming
I am working to get my fork of pykit as close to Python coding standards as possible.  
I have been using the [PEP8](https://peps.python.org/pep-0008/) and ruff to check for these changes.
For Classes & Functions, I will try and maintain a shim module that uses the original names and points
to the new names.  This will help with backward compatibility for a while but I do plan on
deprecating the old names in the future.

The shim lives in `src/pykit/_legacy.py` (aliases) and `src/pykit/_compat.py` (helpers). Old camelCase
names (for example `LogTable.getInteger`, `Logger.startReciever`, `LoggedRobot.useTiming`) still work but
emit a `DeprecationWarning`. User classes that implement the old `toLog`/`fromLog`/`putTable` hooks are
still called. The misspelled module `pykit.logdatareciever` forwards to `pykit.logdatareceiver`.
Not aliased: `Logger.dataRecievers`, the `AlertLogger` subscriber dictionaries, and the
`moduleId`/`moduleType` constructor keywords of `LoggedPowerDistribution`.

## Requirements
Python 3.14 or newer. `LoggedNetworkButton` needs the optional `commands` extra
(`pip install robotpy-pykit[commands]`).
# Collaboration

If you are also interested in contributing to this project, please reach out to me at chip@bcsw.net
and I will try and respond as time allows.