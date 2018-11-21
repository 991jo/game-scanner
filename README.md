#Game Scanner

Gamescanner is a software to find gameservers.

It is written in python with asyncio.

# Outputs

- Output via a webserver and json
- Output for prometheus

# Supported Protocols

- SRCDS Protocol (all SRCDS Games (CounterStrike, Team Fortress2, etc) and several other games like ARK)
- Quake3 Protocal games

# Protocols supported in the future

- different Gamespy versions
- Mumble

# known issues
- some old SRCDS servers report back with the srcds and the goldsource response on the same port. Currently the response processed last will remain in the database
