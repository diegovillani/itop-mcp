import asyncio
import os
import requests
import websockets
from jsonrpcserver import method, async_dispatch

ITOP_URL = os.getenv("ITOP_URL")
ITOP_USER = os.getenv("ITOP_USER")
ITOP_PWD = os.getenv("ITOP_PWD")

def itop_request(payload):
    response = requests.post(ITOP_URL, json={
        "auth_user": ITOP_USER,
        "auth_pwd": ITOP_PWD,
        **payload
    }, verify=False)
    return response.json()

@method
def list_tickets(status="open"):
    payload = {
        "operation": "core/get",
        "class": "UserRequest",
        "key": f"SELECT UserRequest WHERE status='{status}'",
        "output_fields": "id,ref,title,priority,status"
    }
    return itop_request(payload)

async def handler(websocket):
    async for message in websocket:
        response = await async_dispatch(message)
        if response.wanted:
            await websocket.send(str(response))

async def main():
    async with websockets.serve(handler, "0.0.0.0", 9000):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
