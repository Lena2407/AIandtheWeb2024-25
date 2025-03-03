'''
The Pet Chat

A simple messaging channel, where users can post messages with a username. 
The theme of the Channel is to talk about your beloved pets, exchange knowledge
or just have fun exchanging funny moments. This is also done by the active bot 
of the chat, "LovelyCatLady99", who is obsessed with cats but actually avoids
talks about dogs at all costs (she actually manipulated the chat, so that nobody 
is able to use the word dog at all!!). Additionally be aware, that our CatLady-Bot 
sometimes takes a few seconds to answer (5-30s), this is intended to make her style 
more realistic, as it is not easy to chat and take care of your beloved cat at the 
same time ;)

The Chat-Bot answers in a Keyword-Matching Style. When a known pet-keyword is found,
the Bot answers accordingly, otherwise generic answers are posted.

Messages send in the Channel are deleted after one day and inapropriate language
is filtered by default. This also includes messages about dogs, as our CatLady
once banned the topic. 

*Channel* without our wonderful client: http://vm146.rz.uni-osnabrueck.de/client/show?channel=http://vm322.rz.uni-osnabrueck.de/u015/channel.wsgi
Hub with our wonderful *Client*: http://vm322.rz.uni-osnabrueck.de/u015/react-client.html
'''

from flask import Flask, request, render_template, jsonify
import json
import requests
import datetime
from datetime import timedelta
from better_profanity import profanity
import random
import time
import threading


# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!' # change to something random, no matter what

# Create Flask app
app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')  # configuration
app.app_context().push()  # create an app context before initializing db

# local testing
# HUB_URL = 'http://localhost:5555'
# HUB_AUTHKEY = '1234567890'
# CHANNEL_AUTHKEY = '0987654321' 
# CHANNEL_NAME = "The Pet Chat"
# CHANNEL_ENDPOINT = "http://localhost:5001" # don't forget to adjust in the bottom of the file/next row
# PORT = 5001
# CHANNEL_FILE = 'messages.json'
# CHANNEL_TYPE_OF_SERVICE = 'aiweb24:chat'

# deployment
HUB_URL = 'http://vm146.rz.uni-osnabrueck.de/hub'
HUB_AUTHKEY = 'Crr-K24d-2N'
CHANNEL_AUTHKEY = '0987654321' 
CHANNEL_NAME = "The Pet Chat"
CHANNEL_ENDPOINT = "http://vm322.rz.uni-osnabrueck.de/u015/channel.wsgi" 
PORT = 5001
CHANNEL_FILE = 'messages.json'
CHANNEL_TYPE_OF_SERVICE = 'aiweb24:chat'

# Define chatbot responses
reactions = {"parrot": ["Does your parrot talk? My cat would LOVE that... maybe a little too much. 😅", "Parrots are so colorful! Hopefully, your cat doesn't see it as a flying toy.", "A talking pet? Now that’s something my cat and I could argue with all day."], "fish": ["My cat keeps staring at the fish tank like it's a TV show. 🎣", "Better keep the fishbowl out of paw’s reach… for safety reasons.", "I think my cat sees fish as 'animated snacks'."], "hamster": ["A hamster? Hopefully, your cat and hamster have a peace treaty! 🐹", "Tiny, fluffy, and always running… yep, my cat would chase it.", "So… how many near-escapes has your hamster had so far? Be honest."], "snake": ["A snake?! I think my cat would freak out. 😲", "That’s one pet my cat wouldn’t dare mess with!", "If it slithers, my cat stares. I think they’d just have a staring contest forever."], "rabbit": ["A rabbit! Does it hop around like a little cloud?", "Cats and rabbits can be friends… or very confused roommates.", "So much fluff! I bet your rabbit sheds as much as my cat does."], "lizard": ["Lizards are cool, but my cat would just see them as a 'high-speed snack'.", "Does your lizard ever just chill on a warm rock? My cat gets it.", "Scaly and silent… a complete opposite to my demanding furball."], "turtle": ["A turtle! That’s just a cat with armor. Respect. 🐢", "Slow and steady wins the race! Unless my cat knocks it over first.", "Does your turtle ever chase things? My cat would be fascinated."], "ferret": ["Ferrets are basically long, chaotic cats. Sounds fun!", "I bet your ferret and my cat would team up for maximum destruction.", "So sneaky! Ferrets and cats together must mean NOTHING is safe in your house."], "horse": ["A horse?! Okay, now I feel like my cat isn’t as majestic as I thought.", "A horse is like a giant cat, right? Just… a lot bigger and less likely to nap on my keyboard.", "Do horses do zoomies? Because my cat does zoomies. I feel like they’d get along."]}

generic_responses = ["Interesting! Meanwhile, my cat is plotting something again. I just know it.", "I was going to respond, but my cat just knocked something over. Hold on.", "That reminds me… I need to refill the food bowl before I get meowed at.", "Hold on, I’m being summoned by loud, demanding purring noises.", "Huh. Anyway, my cat just stole my seat. Classic."]


@app.cli.command('register')
def register_command():
    global CHANNEL_AUTHKEY, CHANNEL_NAME, CHANNEL_ENDPOINT

    # send a POST request to server /channels
    response = requests.post(HUB_URL + '/channels', headers={'Authorization': 'authkey ' + HUB_AUTHKEY},
                             data=json.dumps({
                                "name": CHANNEL_NAME,
                                "endpoint": CHANNEL_ENDPOINT,
                                "authkey": CHANNEL_AUTHKEY,
                                "type_of_service": CHANNEL_TYPE_OF_SERVICE,
                             }))

    if response.status_code != 200:
        print("Error creating channel: "+str(response.status_code))
        print(response.text)
        return

def check_authorization(request):
    global CHANNEL_AUTHKEY
    # check if Authorization header is present
    if 'Authorization' not in request.headers:
        return False
    # check if authorization header is valid
    if request.headers['Authorization'] != 'authkey ' + CHANNEL_AUTHKEY:
        return False
    return True

@app.route('/health', methods=['GET'])
def health_check():
    global CHANNEL_NAME
    if not check_authorization(request):
        return "Invalid authorization", 400
    return jsonify({'name':CHANNEL_NAME}),  200

# GET: Return list of messages
@app.route('/', methods=['GET'])
def home_page():
    if not check_authorization(request):
        return "Invalid authorization", 400
    # fetch channels from server
    limit_messages()
    return jsonify(welcome_message())

# choose a fitting response for LovelyCatLady99 (generic or fitting to pet-keyword mentioned in previous post)
def respond_to_post(post):
    post_lower = post.lower()
    for keyword, responses in reactions.items():
        if keyword in post_lower: # pet-keyword found
            return random.choice(responses)
    return random.choice(generic_responses) # generic response

# Delaying the Responses of LovelyCatLady99 to make it more realistic
def delayed_bot_response(content):
    delay = random.randint(5, 30)  # Random delay between 5 seconds to 30 seconds
    time.sleep(delay)
    bot_response = {
        'content': respond_to_post(content),
        'sender': "LovelyCatLady99",
        'timestamp': datetime.datetime.now().isoformat(),
        'extra': None
    }
    messages = read_messages()
    messages.append(bot_response)
    save_messages(messages)

# POST: Send a message
@app.route('/', methods=['POST'])
def send_message():
    # fetch channels from server
    # check authorization header
    if not check_authorization(request):
        return "Invalid authorization", 400
    
    # check if message is present
    message = request.json
    if not message:
        return "No message", 400
    if not 'content' in message:
        return "No content", 400
    if not 'sender' in message:
        return "No sender", 400
    if not 'timestamp' in message:
        return "No timestamp", 400
    if not 'extra' in message:
        extra = None
    else:
        extra = message['extra']
    
    # filter messages to guarantee respectful conversations about interesting topics (no dogs allowed!)
    message = filter_messages(message)
    
    # add message to messages
    messages = read_messages()
    messages.append({'content': message['content'],
                     'sender': message['sender'],
                     'timestamp': message['timestamp'],
                     'extra': extra,
                     })
    save_messages(messages)
    
    # send a response from LovelyCatLady99
    if message['sender'] != "LovelyCatLady99":
        threading.Thread(target=delayed_bot_response, args=(message['content'],)).start()
    
    return "OK", 200

def read_messages():
    global CHANNEL_FILE
    try:
        f = open(CHANNEL_FILE, 'r')
    except FileNotFoundError:
        return []
    try:
        messages = json.load(f)
    except json.decoder.JSONDecodeError:
        messages = []
    f.close()
    return messages

def save_messages(messages):
    global CHANNEL_FILE
    with open(CHANNEL_FILE, 'w') as f:
        json.dump(messages, f)

#add a welcome message at the beginning of the channel
def welcome_message():
    welcome_message = {'content': "Welcome to the Pet Chat. Tell us about your beloved pets!",
                     'sender': "Pet Chat",
                     'timestamp': "Before your time",
                     'extra': None,
    }
    messages = read_messages()
    if len(messages) > 0 and welcome_message == messages[0]:
        return messages
    else: 
        messages.insert(0,welcome_message)
        return messages

# filter messages to ensure a respectful exchange on the Channel, and to avoid dog-talk
def filter_messages(message):
    #filter out messages that use profanity and send a reminder that profanity is not allowed
    if profanity.contains_profanity(message['content']): 
        message = {'content': "We don't curse here, darling. Please rephrase or shut it!",
                    'sender': "LovelyCatLady99",
                    'timestamp': message['timestamp'],
        }
        return message
    #filter out all messages that reference dogs, since the cat lady doesn't like dogs
    elif "dog" in message['content']:
        message = {'content': "Hmm, it seems like someone wanted to talk about dogs.... What about cats?",
                    'sender': "LovelyCatLady99",
                    'timestamp': message['timestamp'],
        }
        return message
    else: 
        return message

#delete messages after a day
def limit_messages():
    messages = read_messages()
    now = datetime.datetime.now()
    # Keep only messages from the last 24 hours
    messages = [msg for msg in messages if datetime.datetime.fromisoformat(msg['timestamp']) >= now - timedelta(hours=24)]
    save_messages(messages)  # Save the filtered messages


# Start development web server
# run flask --app channel.py register
# to register channel with hub

if __name__ == '__main__':
    app.run(port=PORT, debug=True)
