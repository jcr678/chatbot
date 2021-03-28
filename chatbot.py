import pickle
import spacy
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
import pickle
import spacy
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
import nltk
def parse_name(nameString):
    nlp = spacy.load('en_core_web_md')
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
def ret_topic_bots(topic_to_doc):
    return "None"

def main():
    nameString = input("Hello, welcome to Austin. What is your name?")
    name = parse_name(nameString)
    print("Hello " + name)
    topic_to_doc = pickle.load( open( "knowledge_base.p", "rb" ) )
    topics = list(topic_to_doc.keys())
    #get name using named entity recognition
    print("I can talk about " + ", ".join(topics[:len(topics)-1]) + ", and " + topics[-1])
    topic_string = input("What topic do you want to talk about?")
    topic_chosen = return_topic_chose(topic_string, topics)
    topic_bots = ret_topic_bots(topic_to_doc)
    print("Sounds good, you want to talk about " + topic_chosen +". when you want to talk about another one of those topics please let me know")
    bot_dict = {topic: None for topic in topics} #put bots here
    while True:
        #let bot on topic talk

        print("Let a given bot talk about topic")

        #when user mentions another topic, switch over to that bot
        user_input = input()

main()
