class WordTranslation:
    def __init__(self, name, translation):
        self.name = name
        self.translation = translation


class WordDefinition:
    def __init__(self, word):
        self.name = word['word']
        self.origin = origin(word)
        self.phonetic = phonetic(word)
        self.definitions = parse_definitions(word)


class WordMeaning:
    def __init__(self, definition):
        self.type = definition_type(definition)
        self.definition = definition_meaning(definition)
        self.example = definition_example(definition)
        self.synonyms = definition_synonyms(definition)


def origin(word):
    try:
        return word['results'][0]['lexicalEntries'][0]['entries'][0]['etymologies'][0]
    except Exception as e:
        print("Error to get origin from word: " + str(e))
        return None


def phonetic(word):
    try:
        return word['results'][0]['lexicalEntries'][0]['pronunciations'][0]['phoneticSpelling']
    except Exception as e:
        print("Error to get phonetic from word: " + str(e))
        return None


def parse_definitions(word):
    definitions = []
    for definition in word['results'][0]['lexicalEntries']:
        definitions.append(WordMeaning(definition))
    return definitions


def definition_type(definition):
    try:
        return definition['lexicalCategory']['text']
    except Exception as e:
        print("Error to get word type: " + str(e))
        return None


def definition_meaning(definition):
    try:
        return definition['entries'][0]['senses'][0].get('definitions', None)
    except Exception as e:
        print("Error to get definition meaning: " + str(e))
        return None


def definition_example(definition):
    examples = []
    try:
        definitions = definition['entries'][0]['senses'][0]['examples']
    except Exception as e:
        print("Error to get definition meaning: " + str(e))
        return None
    for d in definitions:
        examples.append(d.get('text'))
    return examples


def definition_synonyms(definition):
    synonym = []
    try:
        synonyms = definition['entries'][0]['senses'][0]['synonyms']
    except Exception as e:
        print("Error to get definition meaning: " + str(e))
        return None
    for d in synonyms:
        synonym.append(d.get('text'))
    return synonym
