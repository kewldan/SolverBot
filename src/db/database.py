import math
import time

import motor.motor_asyncio

from config import config

client = motor.motor_asyncio.AsyncIOMotorClient(config['bot']['mongo'])
database = client[config['bot']['database']]
users = database['users']


async def get_user(user_id: int, username: str):
    user = await users.find_one({'id': user_id})
    if not user:
        await users.insert_one({
            'id': user_id,
            'username': username,
            'solved': 0,
            'joined': math.floor(time.time())
        })
        user = await users.find_one({'id': user_id})
    return user


async def capture_referral(user_id: int, referral: str):
    await users.update_one({'id': user_id}, {
        '$set': {
            'referral': referral
        }
    })
