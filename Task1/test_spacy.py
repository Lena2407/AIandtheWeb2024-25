import streamlit as st
import spacy
import random

# Load the language model
nlp = spacy.load('en_core_web_lg')

# Fetch the animal list
animal_words = [
    "dog", "cat", "elephant", "lion", "tiger", "bear", "wolf", "fox", "deer", "rabbit",
    "cow", "horse", "goat", "sheep", "pig", "monkey", "gorilla", "kangaroo", "zebra", "giraffe",
    "leopard", "panda", "cheetah", "bison", "squirrel", "otter", "bat", "raccoon", "seal", "whale",
    "dolphin", "penguin", "owl", "parrot", "sparrow", "pigeon", "eagle", "flamingo", "peacock", "duck",
    "chicken", "turkey", "frog", "snake", "lizard", "turtle", "crocodile", "alligator", "shark", "salmon",
    "goldfish", "clownfish", "catfish", "guppy", "swordfish", "marlin", "bass", "trout", "herring", "mackerel",
    "crab", "lobster", "shrimp", "octopus", "squid", "jellyfish", "starfish", "sea lion", "seahorse", "clam",
    "bee", "ant", "butterfly", "ladybug", "dragonfly", "mosquito", "wasp", "grasshopper", "cockroach", "fly",
    "beetle", "praying mantis", "centipede", "scorpion", "spider", "termite", "caterpillar", "firefly", "locust",
    "kiwi", "toucan", "crow", "raven", "magpie", "stork", "crane", "heron", "woodpecker", "blue jay", "cardinal",
    "blue whale", "kangaroo rat", "mule", "alpaca", "llama", "poodle", "bulldog", "beagle", "chihuahua", "pug"
]

# Initialize session state variables
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""  # Initialize user input
if 'username' not in st.session_state:
    st.session_state.username = ""  # Initialize username
if 'guess_count' not in st.session_state:
    st.session_state.guess_count = 0  # Initialize guess count
if 'solution' not in st.session_state:
    st.session_state.solution = random.choice(animal_words)  # Pick a random animal noun as the solution


def reset_game():
    st.session_state.user_input = "" # Clear the user input field
    st.session_state.guess_count = 0  # Reset guess count
    st.session_state.solution = random.choice(animal_words)  # Pick a new random animal noun as the solution
    


# Title
st.title("Guess the Animal")

# Prompt the user for their username
if 'username' not in st.session_state or not st.session_state.username:
    st.session_state.username = st.text_input("Enter your username:", value=st.session_state.username)

# If the user hasn't entered a username, prompt them
if not st.session_state.username:
    st.warning("Please enter your username to start the game.")
else:
    # Display the user's current game state
    st.write(f"Hello, {st.session_state.username}!")
    st.write(f"Solution: {st.session_state.solution}") # debugging
    
    # Input for user guess
    user_guess = st.text_input("What's your guess?", value=st.session_state.user_input,key="user_input").strip().lower()

    # Display the game state
    if user_guess:
        st.session_state.guess_count += 1

        # Convert the strings to spaCy Token objects
        token1 = nlp(user_guess)[0]
        token2 = nlp(st.session_state.solution)[0]

        # Compute and display word similarity
        similarity = token1.similarity(token2)
        st.text(f"Similarity score: {similarity:.4f}")
        st.write(f"Number of guesses: {st.session_state.guess_count}")

        # Check if the guess is correct
        if user_guess == st.session_state.solution:
            st.success(f"Congratulations {st.session_state.username}! You guessed the word '{st.session_state.solution}' correctly in {st.session_state.guess_count} guesses.")
            # Reset solution and guess count for a new game
            st.balloons()


    # Button to start a new game
    st.button("New Word",on_click=reset_game)
