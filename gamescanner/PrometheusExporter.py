import asyncio
from aiohttp import web

database = None

async def handler(request):
    data = database.dump()

    for d in data:
        d["timestamp"] = int(d["timestamp"])

    templates = [
            """gamescanner_maxplayers {{address="{ip}",port="{port}",game_type="{game_type}"}} {max_players} {timestamp}""",
            """gamescanner_server_name {{address="{ip}",port="{port}",game_type="{game_type}"}} {server_name} {timestamp}""",
            """gamescanner_players {{address="{ip}",port="{port}",game_type="{game_type}"}} {players} {timestamp}"""
            ]
    res = "\n".join(t.format(**d) for t in templates for d in data)
    return web.Response(text=res)


async def start_prometheus(loop, db, bind_address, port):
    global database
    database = db
    server = web.Server(handler)

    await loop.create_server(server, bind_address, port)
