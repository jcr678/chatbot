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

#stopwords = stopwords.words('english')
def parse_name(nameString):
    nlp = spacy.load('en')
    doc = nlp(nameString)
    nouns = [noun.text for noun in doc.noun_chunks if "name" not in noun.text] #ignore the noun "name"
    if len(nouns) == 1:
        return nouns[0]
    else:
        nameString = input("Sorry could you repeat that?")
        parse_name(nameString)

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
    nameString = input("Hello, welcome to Austin. What is your name?")
    name = parse_name(nameString)
    print("Hello " + name)

    possible_sentence_starts = ["Let me tell you an Austin fact: ", "A yes " + name, "ect..."]
    while True:
        try:
            print("User response: ")
            bot_input = bot.get_response(input())
            print(random.choice(possible_sentence_starts))
            print("\t" + str(bot_input))

        except(KeyboardInterrupt, EOFError, SystemExit):
            break

main()
