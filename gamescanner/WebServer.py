import asyncio
from aiohttp import web
from json import dumps

database = None

async def handler(request):
    return web.Response(text=dumps(database.dump(), indent=4))


async def start_webserver(loop, db, bind_address, port):
    global database
    database = db
    server = web.Server(handler)

    await loop.create_server(server, bind_address, port)

    while True:
        await asyncio.sleep(100*3600)
