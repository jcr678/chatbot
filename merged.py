import pickle
import random
import spacy
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import math
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import pickle
from chatterbot.trainers import ListTrainer

nlp = spacy.load('en')
#stopwords = stopwords.words('english')
def parse_name(nameString):
    doc = nlp(nameString)
    nouns = [noun.text for noun in doc.noun_chunks if "name" not in noun.text] #ignore the noun "name"
    if len(nouns) == 1:
        return nouns[0]
    else:
        nameString = input("Sorry could you repeat that?")
        parse_name(nameString)

def parse_sentence_starts(user_response, possible_sentence_starts):
    doc = nlp(user_response)
    #when user says an adjective repeat it back to them!
    adjectives = [random.choice(["True, that is very " + str(d), "Oh wow very " + str(d)]) for d in doc if d.pos_ == "ADJ"]
    numbers = ["That is an interesting number... " + str(d) for d in doc if d.pos_ == "NUM"]
    interjections = [random.choice([str(d) + "!", str(d)])
                                for d in doc if d.pos_ == "INTJ"]
    dont_understands = ["I dont understand that word really, " + str(d) for d in doc if d.pos_ == "X"]
    locations = ["What an interesting place " + str(d)
                                for d in doc.ents if d.label_ == "GPE" or d.label_ == "LOC"]
    punctuations = [str(d) for d in doc if d.pos_ == "PUNCT"]
    possible_sentence_starts.extend(adjectives)
    possible_sentence_starts.extend(numbers)
    possible_sentence_starts.extend(interjections)
    if "?" in user_response: #let user know I saw that its a question
        print("Ah yes that is a good question...")
    if "!" in user_response:
        print("Please stop screaming")
    if len(punctuations) == 0:
        print("Why arent you using punction stupid")
    if len(locations) >= 1:
        print(random.choice(locations))
    if len(dont_understands) >= 1:
        print(random.choice(dont_understands))
        return possible_sentence_starts
    if len(adjectives) >=1:
        print(random.choice(adjectives))
        return possible_sentence_starts
    if len(interjections) >=1:
        print(random.choice(interjections))
        return possible_sentence_starts
    if len(numbers) >= 1:
        print(random.choice(numbers))
        return possible_sentence_starts
    print(random.choice(possible_sentence_starts))
    return possible_sentence_starts

def return_topic_chose(topic_string, topics):
    #stemmer = PorterStemmer()
    wnl = WordNetLemmatizer()
    topic_string_tokens =  [str(t).lower() for t in nltk.word_tokenize(topic_string)]
    topic_string_lemma = [wnl.lemmatize(t)  for t in topic_string_tokens]
    #do like a regex search but stemmed to take care of words that end with "s" or "ing"
    topics_lemma = {wnl.lemmatize(t):t for t in topics}
    #print(topics_lemma)
    for lem in list(topics_lemma.keys()):
        if lem in topic_string_lemma:
            return topics_lemma[lem]
    topic_string = input("Sorry I didnt get that can you repeat that?")
    return return_topic_chose(topic_string, topics)
def main():
    topic_to_doc = pickle.load( open( "knowledge_base.p", "rb" ) )
    bot = ChatBot(
        'Buddy',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///database.sqlite3',
        logic_adapters=[
            'chatterbot.logic.BestMatch'],
    )


    #trainer.train(topic_to_doc['university'])
    keys = list(topic_to_doc.keys())
    to_train = []
    for k in keys:
        #print(k)
        #print(len(topic_to_doc[k]))
        to_train.extend(topic_to_doc[k])
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train(
            "chatterbot.corpus.english.greetings",
            "chatterbot.corpus.english.conversations"
    )
    trainer = ListTrainer(bot)
    trainer.train(to_train)
    nameString = input("Hello, welcome to Austin. Ill tell you about the city. What is your name?")
    name = parse_name(nameString)
    print("Hello " + name)
    possible_sentence_starts = ["Okay, " + name]
    i = 0
    while True:
        try:
            #print("User response: ")
            user_response = input("User response: ")
            bot_input = bot.get_response(user_response)
            possible_sentence_starts = parse_sentence_starts(user_response, possible_sentence_starts)
            print("Let me tell you another Austin fact! Please ask about Austin.")
            print("\t" + str(bot_input))

        except(KeyboardInterrupt, EOFError, SystemExit):
            break

main()
