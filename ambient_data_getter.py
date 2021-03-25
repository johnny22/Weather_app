import asyncio
from aiohttp import ClientSession
from aioambient import Client
from datetime import date

async def main() -> None:
    """Create a session"""
    client = Client("96255560b32d46bf82101c3a42a9213ffae52644090e485eac958e2c4e55e88a",    "65a5fd146d2a4bc09640a1fdf8c44887595fb4a5b0504693b8554e12a4ca2d87")
    await client.api.get_devices()
    print ('hi')


asyncio.run(main())
