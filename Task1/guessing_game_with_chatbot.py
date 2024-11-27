import streamlit as st
import random
import spacy
import pandas as pd
import os
from openai import OpenAI

# Load spaCy model
@st.cache_resource
def load_nlp():
    return spacy.load('en_core_web_lg')

nlp = load_nlp()

# List of nouns to choose from
nouns = [
    "cat", "dog", "house", "tree", "book", "car", "phone", "computer",
    "chair", "table", "bird", "flower", "sun", "moon", "star", "cloud",
    "mountain", "river", "ocean", "forest", "tomato","apple", "jacket", 
    "airplane", "banana", "guitar", "piano", "violin", "elephant",  "rose", 
    "shoe", "cake", "cheese", "pizza", "ice cream", "coffee",  "hand", "hat",
    "snow", "boat", "train", "door", "duck", "fish", "farm", "teacher", "baby", 
    "doctor", "lemon", "umbrella", "pillow"
]

score_file_path = 'statistics.csv'

def reset():
    # Reset session state variables (except username)
    st.session_state.solution = random.choice(nouns)
    st.session_state.game_won = False
    st.session_state.guess_count = 0
    st.session_state.previous_similarities = []
    st.session_state.similarity_count = []
    st.session_state.guesses = []
    st.session_state.chat_history = []  # Clear chat history when resetting
    st.info("A new word was chosen!")
    

# Initialize session state variables
if 'username' not in st.session_state:
    st.session_state.username = ""

if 'solution' not in st.session_state:
    st.session_state.solution = random.choice(nouns)
    
if 'game_won' not in st.session_state:
    st.session_state.game_won = False
    
if 'guess_count' not in st.session_state:
    st.session_state.guess_count = 0

if 'previous_similarities' not in st.session_state:
    st.session_state.previous_similarities = []

if 'similarity_count' not in st.session_state:
    st.session_state.similarity_count = []

if 'guesses' not in st.session_state:
    st.session_state.guesses = []

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


# Title and instructions
st.title("Best Word Guessing Game Ever Seen 😎")

# Prompt the user for their username if not already set
if not st.session_state.username:
    st.session_state.username = st.text_input("Enter your username:", key="username_input")
    
    # Prevent further interaction until username is entered
    if not st.session_state.username:
        st.warning("Please enter your username to start the game.")
        st.stop()

st.write(f"Hello, {st.session_state.username}!")
st.write(f"Welcome to the game. Try to guess the word I'm thinking of by entering your guesses in the left textbox. You can also ask yes/no questions to help you guess the word in the right textbox.")

############ TWO COLUMNS ###########################################################################
# Create two columns
col1, col2 = st.columns(2)
with col1:

    # Create a form for input
    with st.form(key='guess_form'):
        user_guess = st.text_input("Enter your guess:", key="guess_input").lower()
        submit_button = st.form_submit_button("Submit Guess")

    # Handle form submission
    if submit_button and user_guess:
        st.session_state.guess_count += 1
        
        # Compute word similarity
        token1 = nlp(user_guess)[0]
        token2 = nlp(st.session_state.solution)[0]
        similarity = token1.similarity(token2)
        
        # Store similarity for tracking progress
        st.session_state.previous_similarities.append((user_guess, similarity))
        st.session_state.similarity_count.append(similarity)
        st.session_state.guesses.append(user_guess)

        
        # Inside the if condition where the guess is correct
        if user_guess == st.session_state.solution:
            # Save game stats
            stats_df = pd.DataFrame({
                'quantity': [st.session_state.guess_count],
                'quality': [st.session_state.similarity_count],
                'guesses': [st.session_state.guesses]
            }, index=[st.session_state.username])
            
            file_exists = os.path.exists(score_file_path)
            stats_df.to_csv(score_file_path, mode='a', header=not file_exists)
            
            # Display success message
            st.balloons()
            st.success(f"🎉 Congratulations {st.session_state.username}! You guessed the word '{st.session_state.solution}' in {st.session_state.guess_count} guesses!")
            
            # Reset the game while preserving the username
            reset()


    
        else:
            st.warning("Try again!")
            
    
    #st.write("Debug - Current solution:", st.session_state.solution)
    
    # Show guess history as a colored table
    if st.session_state.previous_similarities:
        st.write("### Guess History")
        
        # Create DataFrame for guess history
        guess_history_df = pd.DataFrame(
            st.session_state.previous_similarities, 
            columns=['Guess', 'Similarity']
        ).sort_values('Similarity', ascending=False)
        
        # Style the DataFrame with a color gradient
        def color_gradient(val):
            """
            Creates a color gradient from red (low similarity) to green (high similarity)
            Uses rgba to allow for transparency
            """
            # Normalize the value between 0 and 1
            normalized = min(max(val, 0), 1)
            
            # Red to green gradient
            red = int(255 * (1 - normalized))
            green = int(255 * normalized)
            
            return f'background-color: rgba({red}, {green}, 0, 0.5)'

        # Apply styling and display
        styled_df = guess_history_df.style.applymap(
            color_gradient, 
            subset=['Similarity']
        ).format({'Similarity': '{:.4f}'})
        
        st.dataframe(styled_df)


############### 2nd Column ##############################################################

with col2:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    model = "gpt-4o-mini"

    #st.write("You can ask me yes/no questions, that will help you guess the correct word.")

    solution = st.session_state.solution

    # Function to ask GPT to answer yes/no based on predefined animal
    def ask_llm(question, solution):
        prompt = f"Answer the following yes/no question based on the word: {solution}.\n. If it is not a yes/no question, say: I can only answer yes/no questions. Question: {question}\nAnswer (Yes/No):"
        
        try:
            # Call OpenAI GPT model for answering the question
            response = client.chat.completions.create(
                model = model,  # "gpt-4" or "gpt-3.5-turbo" or "gpt-4o-mini", depending on access
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0  # Set to 0 to make answers deterministic (yes/no answers)
            )
            # Extract the response
            answer = response.choices[0].message.content
            return answer
        except Exception as e:
            print(f"Error with OpenAI API: {str(e)}")
            return "I couldn't understand that question."
        

    # Initialize session state for chat history and input field
    if "history" not in st.session_state:
        st.session_state["history"] = []

    # Create a form for input
    with st.form(key='chatbot_form'):
        user_question = st.text_input("Ask your question:", key="user_question").lower()
        submit_question_button = st.form_submit_button("Submit Question")

    # When user submits input
    if user_question and submit_question_button:
            answer_question = ask_llm(user_question, solution)
            st.session_state.chat_history.append({"user": user_question, "bot": answer_question})

    # Display chat history
    st.write("### Chat History")

    # Construct the scrollable container with messages as raw HTML
    history_html = """
    <style>
    .scrollable-container {
        height: 350px;
        overflow-y: auto;
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 5px;
        background-color: #f9f9f9;
        font-family: Arial, sans-serif;
        font-size: 14px;
    }
    .message {
        margin-bottom: 5px;
        padding: 5px;
        background-color: #e8e8e8;
        border-radius: 3px;
        word-wrap: break-word;
    }
    </style>
    <div class="scrollable-container" id="scrollable-container">
    """

    # Add each message to the container
    for chat in st.session_state.chat_history:
        msg1 = f"You: {chat['user']}"
        msg2 = f"Bot: {chat['bot']}"
        history_html += f'<div class="message">{msg1}</div>'
        history_html += f'<div class="message">{msg2}</div>'
    history_html += "</div>"

    # Render the scrollable container with messages
    st.markdown(history_html, unsafe_allow_html=True)
