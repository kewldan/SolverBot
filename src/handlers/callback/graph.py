import io
from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import CallbackQuery, BufferedInputFile
from matplotlib import pyplot as plt

from config import config
from database import User

graph_router = Router()
plt.style.use('dark_background')


@graph_router.callback_query(F.data == 'graph', F.from_user.id.in_(config.bot.owners))
async def on_graph_callback(query: CallbackQuery):
    users = [*map(lambda doc: doc.joined, await (User.find_all().to_list()))]
    date = datetime.now() - timedelta(weeks=3)

    dates, values = [], []

    while date <= datetime.now():
        dates.append(date)
        values.append(len([x for x in users if x < date]))
        date += timedelta(hours=1)

    fig, ax1 = plt.subplots()

    ax1.plot(dates, values, color='tab:green')
    ax1.set_xlabel('Дата')
    ax1.set_ylabel('Количество')
    ax1.set_title(f'Пользователи на {datetime.now().strftime('%H:%M:%S %d.%m.%Y')}')
    ax1.fill_between(dates, values)
    plt.gcf().autofmt_xdate()
    with io.BytesIO() as buf:
        plt.savefig(buf, format='png', dpi=400)
        buf.seek(0)
        graph_file = BufferedInputFile(buf.read(), filename="graph.png")
        await query.message.answer_photo(graph_file)
