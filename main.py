
from fastapi import FastAPI, Request
import telegram
from telegram.ext import Dispatcher, MessageHandler, Filters
from config import TELEGRAM_TOKEN, WEBHOOK_URL
from bot_logic import handle_text

app = FastAPI()
bot = telegram.Bot(token=TELEGRAM_TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

@app.post("/webhook")
async def webhook(request: Request):
    update = telegram.Update.de_json(await request.json(), bot)
    dispatcher.process_update(update)
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Smart Transport Bot is running."}

@app.on_event("startup")
async def set_webhook():
    bot.delete_webhook()
    bot.set_webhook(WEBHOOK_URL)
