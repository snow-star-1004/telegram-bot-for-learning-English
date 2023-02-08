import configparser

config = configparser.ConfigParser()
config.read('bot.ini')

TOKEN = config['Telegram']['token']
PROXY = config['Telegram']['proxy']
DIALOG_FLOW_NAME = config['DialogFlow']['name']
DIALOG_FLOW_LANGUAGE = config['DialogFlow']['language']
DIALOG_FLOW_TOKEN = config['DialogFlow']['token']
OXFORD_ID = config['Oxford']['id']
OXFORD_APP = config['Oxford']['app']