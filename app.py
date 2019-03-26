import asyncio
import json
import random

import aioredis

loop = asyncio.get_event_loop()


async def run(ev_loop):
    conn = await aioredis.create_connection('redis://localhost/2', loop=ev_loop)

    redis = aioredis.Redis(conn)

    print("Starting app server")
    while ev_loop.is_running():
        queue_name, data = await redis.blpop('avalanche_messages')
        data = json.loads(data)

        msg_type, msg_sender, response_queue, msg_full = data.get('type'), data.get('conn_id'), data.get('response_queue'), data

        print(f"{msg_type} {msg_sender} {msg_full.get('message', '')}")

        name = str(random.choice(range(10, 99)))

        if msg_type == "CONNECTED":
            print("Sending direct message")
            response = {
                "conn_id": msg_sender,
                "type": "MESSAGE",
                "message": f"Welcome to the lobby {name}"
            }
            await redis.rpush(response_queue, json.dumps(response))

            join_msg = {
                "conn_id": msg_sender,
                "action": "ROOM_JOIN",
                "room": "lobby"
            }

            await redis.publish_json("avalanche_room_broadcasts", join_msg)
            print("Broadcasted room join")

            broadcast_message = {
                "conn_id": msg_sender,
                "action": "MESSAGE",
                "room": "lobby",
                "message": f"{name} has joined the lobby"
            }
            # Make sure that the message queue you are using preserves broadcast order,
            # otherwise the broadcasted message could be lost as it would get there before
            # the room_join message
            await redis.publish_json("avalanche_room_broadcasts", broadcast_message)

    conn.close()
    await conn.wait_closed()


loop.run_until_complete(run(loop))
