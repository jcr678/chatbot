from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot(
    'HelloWorld',
)

# Create a new trainer for the chatbot
#trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot based on the english corpus
#trainer.train("chatterbot.corpus.english")

# Get a response to an input statement

while True:
    try:
        bot_input = chatbot.get_response(input())
        print(bot_input)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break
'''
while True:
    response = chatbot.get_response("Hello, I am Jacob.")
    print(response)'''
