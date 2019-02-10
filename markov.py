import random
import json
from collections import defaultdict

#Generate Message

def generate_message(mchain, name, count = 100):
    word1 = random.choice(list(mchain[name].keys()))
    message = word1.capitalize()

    while len(message.split(' ')) < count:
        if word1 in mchain[name]:
            word2 = random.choice(mchain[name][word1])
            word1 = word2
            message += ' ' + word2
        else:
            break
    
    return message

