import pickle
import spacy
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import math


#stopwords = stopwords.words('english')
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
'''
def ret_topic_bots(topic_to_doc):
    return "None"

def create_tf_dict(doc):
    tf_dict = {}
    concat_doc = ""
    for line in doc:
        line = line.strip('\n')
        concat_doc = concat_doc + " "  + line
    tokens = word_tokenize(concat_doc)
    tokens = [w for w in tokens if w.isalpha() and w not in stopwords]
    token_set = set(tokens)
    tf_dict = {t:tokens.count(t) / len(tokens) for t in token_set}
    return tf_dict, tokens, list(token_set)

def create_tfidf(tf, idf):
    tf_idf = {}
    for t in tf.keys():
        tf_idf[t] = tf[t] * idf[t]

    return tf_idf

def important_words(topic_to_doc):
    for topic in list(topic_to_doc.keys()):
        doc = topic_to_doc[topic]
        tf, tokens, token_unique = create_tf_dict(doc)
        idf = {}
        for t in token_unique:
            num_sents = len(doc)
            num_sentences_with_term = 0
            for sentence in doc:
                if t in sentence:
                    num_sentences_with_term+=1
            idf[t] = math.log((1+num_sents) / (1+num_sentences_with_term))
        tf_idf = create_tfidf(tf, idf)
        doc_term_weights = sorted(tf_idf.items(), key=lambda x:x[1])[0:5]
        print("Topic is: "+ topic)
        print(doc_term_weights)
    return "None"
'''
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
    topic_bots = topic_to_doc
    #important = important_words(topic_to_doc)
    print("Sounds good, you want to talk about " + topic_chosen + ". when you want to talk about another one of those topics please let me know")
    i = 0
    #save other state variables
    # for example adjectives the user mentioned ie "Thats really descriptive, " + adjective
    possible_sentence_starts = ["Let me tell you a zilla fact: ", "A yes " + name, "ect..."]
    while True:
        user_input = input()
        chatterbot_english_responds() #user thinks their talking to zilla bot, but its really generic english
        print(possible_sentence_starts[random_index])
        print(topic_bots[topic][i])
        i = i + 1
        if i >= len(topic_bots[topic]):
            print("Lets talk about a different topic")
            topic_string = input("Lets talk about something else. What topic do you want to talk about?")
            topic_chosen = return_topic_chose(topic_string, topics)
            i = 0


main()
