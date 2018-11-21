# Game Scanner

Game Scanner is a software to find gameservers.

It is written in python with asyncio.

# Requirements

Only python3 (3.5 to be specific) and aiohttp is needed.

## Arch linux

    pacman -S python python-aiohttp

## Debian (and probably also Ubuntu)

    apt install python3 python3-aiohttp

# Features

- Finds games based on the following protocols:
  - SRCDS Protocol (SRCDS Games (CSGO, Team Fortress2, etc) and many more (e.g. ARK, Conan Exiles)
  - Quake3 Protocol games
- Output via a webserver and json
- Output as a prometheus exporter (only player count, max players and bot count currently)

# How to run it?

1. create a `config.py` in `gamescanner/config.py`
   An example can be found in the `gamescanner/config-example.py` file.
   A description of the config options is also in this file.
2. Run `python3 gamescanner/GameScanner.py`
3. be happy and find the output on the configured webserver or via the integrated
   prometheus exporter

# known issues
- some old SRCDS servers report back with the srcds and the goldsource response on the same port. Currently the response processed last will remain in the database

# Protocols supported in the future

- different Gamespy versions
- Mumble
