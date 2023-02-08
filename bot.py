import time
from datetime import datetime

import schedule
import telebot
from telebot import apihelper

import api.dialogflow_api as dialog_flow
import api.english_api as english_api
from common import message_generator, security

bot = telebot.TeleBot(security.TOKEN)
apihelper.proxy = {'https': security.PROXY}

commands = {  # command description used in the "help" command
    'start': 'Start learning English',
    'help': 'Information about the available commands',
    'meaning': 'Get word meaning and full information',
    'translate': 'Get translation',
    'subscribe': 'Start learning English by 5 words everyday',
    'unsubscribe': 'Stop sending 5 words'
}


@bot.message_handler(commands=['start'])
def command_start(message):
    bot.send_sticker(message.chat.id, message_generator.Sticker.start)
    bot.send_message(message.chat.id, message_generator.Message.greeting)
    command_help(message)


@bot.message_handler(commands=['subscribe'])
def command_subscribe(message):
    try:
        bot.send_message(message.chat.id, message_generator.Message.learn_5_words)
        current_time = datetime.now().strftime('%H:%M')
        schedule.every().day.at(current_time).do(subscribe_message, message).tag(message.chat.id)
        # schedule.every(10).seconds.do(subscribe_message, message).tag(message.chat.id)
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        print("subscribing error: " + str(e) + "\n")


@bot.message_handler(commands=['unsubscribe'])
def command_unsubscribe(message):
    try:
        schedule.clear(message.chat.id)
        bot.send_message(message.chat.id, message_generator.Message.stop_learn_5_words)
    except Exception as e:
        print("unsubscribe error: " + str(e) + "\n")


@bot.message_handler(commands=['help'])
def command_help(message):
    bot.send_message(message.chat.id, message_generator.message_help(commands))


@bot.message_handler(commands=['meaning'])
def command_meaning(message):
    bot.register_next_step_handler_by_chat_id(message.chat.id, callback=command_meaning_handler)


def command_meaning_handler(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')  # show the bot "typing" (max. 5 secs)
        bot.send_message(message.chat.id, english_api.parse_word_definition(message.text.lower()),
                         parse_mode='Markdown')
    except Exception as e:
        print("Error with getting word definition: " + str(e))
        bot.send_message(message.chat.id, message_generator.Message.word_not_found)


@bot.message_handler(commands=['translate'])
def command_translate(message):
    bot.register_next_step_handler_by_chat_id(message.chat.id, callback=command_translate_handler)


def command_translate_handler(message, translation_from_command=True):
    try:
        bot.send_chat_action(message.chat.id, 'typing')  # show the bot "typing" (max. 5 secs)
        if translation_from_command:
            bot.send_message(message.chat.id, english_api.translate(message.text.lower()))
        else:
            word = message.text.split('"')[1]
            bot.send_message(message.chat.id, message_generator.Message.translate_word + word)
            bot.send_message(message.chat.id, english_api.translate(word))
    except Exception as e:
        print("Error with getting word translation: " + str(e))
        bot.send_message(message.chat.id, message_generator.Message.word_not_translated)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def send_message(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')  # show the bot "typing" (max. 5 secs)
        if 'translate' in message.text.lower():
            command_translate_handler(message, False)
        else:
            bot.send_message(message.chat.id, dialog_flow.call_small_talk(message.text.lower()))
    except Exception as e:
        print("Error with getting answer from small talk: " + str(e))
        bot.send_sticker(message.chat.id, message_generator.Sticker.error)
        bot.send_message(message.chat.id, message_generator.Message.unknown_answer)


def subscribe_message(message):
    number_words = 5
    bot.send_message(message.chat.id, english_api.get_random_words(number_words))


bot.polling()
