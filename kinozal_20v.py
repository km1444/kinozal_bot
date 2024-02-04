import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, ContextTypes, CommandHandler)
# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import requests
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
load_dotenv()
secret_token = os.getenv('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# URL_players = 'https://45seasons.ru/api/players/'
# URL_players_most_goals = 'https://45seasons.ru/api/players_most_goals/'
# URL = 'https://45seasons.ru/api/players/'

url_adr = 'https://qmxnntikcog.kinozal4me.info/top.php?sid=fP7U4sk9&j=&t=1&d=0&k=0&f=0&w=0&s=0'

# buttons = ReplyKeyboardMarkup([
#     ['/players_most_goals', '/best_players'],
#     ['/start']], resize_keyboard=True)


async def start_app(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    await context.bot.send_message(
        chat_id=job.chat_id,
        text="I'm a bot, please talk to me!"
    )


async def start_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    context.job_queue.run_repeating(add_data, 60000, chat_id=chat_id)
    text = "App start succesfull!"
    await update.effective_message.reply_text(text)


async def add_data(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    url = url_adr
    response = requests.get(url)
    src = response.text
    with open('second.html', 'w') as file:
        file.write(src)
    with open('second.html') as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    quotes = soup.find(class_='bx1').find_all('a')
    count = 1
    imdb_dict = {}
    for item in quotes:
        item_text = item.get('title').split('/')[0]
        item_href = 'https://qmxnntikcog.kinozal4me.info' + item.get('href')
        req = requests.get(url=item_href)
        src_movie = req.text
        soup = BeautifulSoup(src_movie, 'lxml')
        quotes_imdb = soup.find_all('a', target='_blank')
        if quotes_imdb[1].text[:4] == 'IMDb':
            imdb = quotes_imdb[1].text[4:7]
            rep = '—'
            if rep in imdb:
                imdb = imdb.replace(rep, '0')
            imdb_dict[item_text] = [float(imdb), item_href]
        print(item_text)
        count += 1
        if count == 11:
            break
    imdb_dict_sort = dict(
        sorted(imdb_dict.items(), key=lambda item: item[1], reverse=True)
    )
    for key, value in imdb_dict_sort.items():
        text = f'{key} {value[0]}'
        await context.bot.send_message(
            chat_id=job.chat_id, text=text
        )


if __name__ == '__main__':
    application = ApplicationBuilder().token(secret_token).build()
    start_message_handler = CommandHandler('start_message', start_message)
    add_data_handler = CommandHandler('add_data', add_data)
    application.add_handler(start_message_handler)
    application.add_handler(add_data_handler)
    application.run_polling()
