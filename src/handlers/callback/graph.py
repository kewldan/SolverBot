import io
import time
from datetime import datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery, BufferedInputFile
from matplotlib import pyplot as plt

import api
from db import database

graph_router = Router()
plt.style.use('dark_background')


@graph_router.callback_query(F.data == 'graph', F.from_user.id.in_(api.config.bot.owners))
async def graph(query: CallbackQuery):
    users = [*map(lambda doc: doc['joined'], await (database.users.find().to_list(None)))]
    unix = min(users)

    dates, values = [], []

    while unix <= time.time():
        date = datetime.fromtimestamp(unix)
        dates.append(date)
        values.append(len([x for x in users if x < unix]))
        unix += 3600

    fig, ax1 = plt.subplots()

    ax1.plot(dates, values, color='tab:green')
    ax1.set_xlabel('Дата')
    ax1.set_ylabel('Количество')
    ax1.set_title(f'Пользователи на {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}')
    ax1.fill_between(dates, values)
    plt.gcf().autofmt_xdate()
    with io.BytesIO() as buf:
        plt.savefig(buf, format='png', dpi=400)
        buf.seek(0)
        graph_file = BufferedInputFile(buf.read(), filename="graph.png")
        await query.message.answer_photo(graph_file)
