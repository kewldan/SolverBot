import asyncio
import json
import logging
import os.path
import shutil

import aiofiles
from pydantic.v1.utils import deep_update

config_file = 'data/config.json'
default_config_file = os.path.join('assets', 'default_config.json')

config = {}


async def reload():
    global config
    async with aiofiles.open(default_config_file, 'r', encoding='utf-8') as f:
        config = json.loads(await f.read())

    if os.path.exists(config_file):
        async with aiofiles.open(config_file, 'r', encoding='utf-8') as f:
            user_config = json.loads(await f.read())
            config = deep_update(config, user_config)
        async with aiofiles.open(config_file, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(config, ensure_ascii=True, sort_keys=True, indent=4))
    else:
        shutil.copyfile(default_config_file, config_file)
        logging.error('Config was created')
        exit(0)


asyncio.run(reload())
