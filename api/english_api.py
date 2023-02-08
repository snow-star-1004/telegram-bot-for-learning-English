import json
import random

import googletrans
import langid
import requests

from common import message_generator, security
from api.word import WordTranslation, WordDefinition


def __load_words():
    word_list = []
    try:
        with open('api/words.json') as f:
            words = json.load(f)
        for word in words['data']:
            word_list.append(WordTranslation(word['name'], word['detail']))
        return word_list
    except Exception as e:
        raise Exception('Can not load words ' + str(e))


word_dictionary = __load_words()


def get_random_words(number):
    random_numbers = random.sample(word_dictionary, number)
    result = ""
    for word in random_numbers:
        result = result + message_generator.Emoji.zap + word.name + "\n" + word.translation + "\n\n"
    return result


def __parse_word_definition(word):
    language = "en-gb"
    url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + word.lower()
    response = requests.get(url, headers={"app_id": security.OXFORD_ID, "app_key": security.OXFORD_APP})
    if response.status_code != 200:
        raise Exception('Can not load words due to error: {}'.format(response.json().get('message')))
    return WordDefinition(response.json())


def __parse_information(definition_name, definition):
    if definition is not None:
        if type(definition) is not str:
            return definition_name + " " + ' / '.join(definition) + "\n"
        else:
            return definition_name + " " + definition + "\n"
    else:
        return ""


def parse_word_definition(message):
    word = __parse_word_definition(message)
    word_definition = __parse_information(message_generator.Emoji.zap, "*" + word.name + "*") + "\n" + \
                      __parse_information("[", word.origin + "]") + "\n" + \
                      __parse_information("**", word.phonetic + "**") + "\n\n"

    for definition in word.definitions:
        word_definition = word_definition + \
                          __parse_information(message_generator.Emoji.check, definition.type) + \
                          __parse_information("*Meaning:*", definition.definition) + \
                          __parse_information("*Example:*", definition.example) + \
                          __parse_information("*Synonyms:*", definition.synonyms) + "\n"
    return word_definition


def translate(word):
    lang = langid.classify(word)
    translation_language = 'ru' if lang[0] == 'en' else 'en'
    translator = googletrans.Translator()
    return translator.translate(word, dest=translation_language).text
