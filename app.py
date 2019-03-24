import asyncio
import json

import aioredis

loop = asyncio.get_event_loop()


async def run(ev_loop):
    conn = await aioredis.create_connection('redis://localhost/2', loop=ev_loop)

    redis = aioredis.Redis(conn)

    while ev_loop.is_running():
        queue_name, data = await redis.blpop('avalanche_messages')
        data = json.loads(data)

        msg_type, msg_sender, msg_full = data.get('type'), data.get('conn_id'), data

        print(f"Got {msg_type} type message from {msg_sender}, {msg_full}")

        if msg_type == "MESSAGE" and msg_full.get('message', '').lower() == "ping":
            print("Sending pong")
            response = {
                "conn_id": msg_sender,
                "type": "MESSAGE",
                "message": "pong"
            }
            await redis.lpush("avalanche_responses", json.dumps(response))

    conn.close()
    await conn.wait_closed()


loop.run_until_complete(run(loop))
