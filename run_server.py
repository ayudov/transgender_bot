from flask import Flask, request
from config import *
from bot_handlers import bot
from telebot import types


app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    bot.remove_webhook()
    bot.set_webhook(url="https://25207845.ngrok.io/{}".format(TOKEN))
    return "Hey, I'm working!)", 200


@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port='8443')
