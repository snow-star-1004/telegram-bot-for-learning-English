from emoji import emojize


class Sticker:
    start = "CAACAgIAAxkBAAJlvV62spvcM24UodEoOMaOBqm3VQ2JAAIMAAPLm8wYVeUb04BjW2wZBA"
    error = "CAACAgIAAxkBAAJlv162srQ4pKVlw_GTpi2LWHi7udoHAAILAAPLm8wYHXFmgN4_n68ZBA"
    smile = "CAACAgIAAxkBAAJlwV62ss5B_1oEs4p6WJ6AVkquBP0hAAIKAAPLm8wYZd7Zi1a78BwZBA"


class Emoji:
    zap = emojize(":zap:", use_aliases=True)
    smile = emojize(":relaxed:", use_aliases=True)
    sad = emojize(':pensive:', use_aliases=True)
    confused = emojize(':face_with_monocle:', use_aliases=True)
    check = emojize(":white_check_mark:", use_aliases=True)


class Message:
    greeting = "Hey! This is Baya Bot, let's learn English " + Emoji.smile
    api_error = "Oh well ... Something went wrong " + Emoji.sad
    word_not_found = "Sorry, I can't find definitions for the word you were looking for " + Emoji.confused
    word_not_translated = "Sorry, I can't translate word " + Emoji.sad
    unknown_answer = "Oh well, I missed what you said. What was that? " + Emoji.confused
    learn_5_words = "Let's learn 5 words everyday " + Emoji.smile
    stop_learn_5_words = "Finished. I hope you will continue learning words " + Emoji.smile
    translate_word = "Try to translate: "


def message_help(commands):
    help_text = "The following commands are available: \n\n"
    for key in commands:
        help_text += "/" + key + ": " + commands[key] + "\n"
    return help_text
