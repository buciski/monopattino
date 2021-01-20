import logging
import sys

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, Filters, CommandHandler, MessageHandler, CallbackQueryHandler


class MonoBot:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    # define a command callback function
    def start(self,update, context):
        context.bot.send_message(chat_id=update.message.chat_id, text="risposta a start cmd")

    def echo(self,update, context):
        context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text + " qualcosa")

    def option(self,update, context):
        button = [
            [InlineKeyboardButton("text 1", callback_data="1")],
            [InlineKeyboardButton("text 2", callback_data="2")],
            [InlineKeyboardButton("text 3", callback_data="3")],
        ]
        reply_markup = InlineKeyboardMarkup(button)
        context.bot.send_message(chat_id=update.message.chat_id, text="scegli..", reply_markup=reply_markup)

    def button(self,update, context):
        query = update.callback_query
        # context.bot.send_message(chat_id=query.message.chat_id, text="vitto " + query.data)
        # use this below in order to hide option
        context.bot.edit_message_text(chat_id=query.message.chat_id, text="vitto " + query.data,
                                      message_id=query.message.message_id)

    def get_location(self,update, context):
        button = [[KeyboardButton("share location", request_location=True)]]
        reply_markup = ReplyKeyboardMarkup(button)
        context.bot.send_message(chat_id=update.message.chat_id, text="share location?", reply_markup=reply_markup)

    def location(self,update, context):
        lat = update.message.location.latitude
        lon = update.message.location.longitude
        context.bot.send_message(chat_id=update.message.chat_id, text="lat:" + str(lat) + " lon:" + str(lon),
                                 reply_markup=ReplyKeyboardRemove())


if __name__ == "__main__":
    bot = MonoBot()
    # first of all take token in order to authenticate
    # check new messages --> polling
    updater = Updater(token=sys.argv[1])
    # allows to register handler --> command, text, video, audio, ...
    dispatcher = updater.dispatcher
    # CORE <<-----------
    # create a command headler and command heandler to dispatcher ###ORDER LIST IS IMPORTANT!!
    updater.dispatcher.add_handler(CommandHandler('start', bot.start))
    updater.dispatcher.add_handler(CommandHandler('option', bot.option))
    updater.dispatcher.add_handler(CommandHandler('location', bot.get_location))
    updater.dispatcher.add_handler(MessageHandler(Filters.location, bot.location))
    updater.dispatcher.add_handler(CallbackQueryHandler(bot.button))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, bot.echo))
    # start polling
    updater.start_polling()
