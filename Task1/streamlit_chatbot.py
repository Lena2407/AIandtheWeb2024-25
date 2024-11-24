import streamlit as st
from openai import OpenAI


########### animal to guess #############################
predefined_animal = "dog"

########### set your openai api key and version #########
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
model = "gpt-4o-mini"


st.title("Chatbot: Animal Guessing Assistant")
st.write("Welcome to the Animal Guessing Game!")
st.write("You can ask me yes/no questions, that will help you guess the correct animal.")

# Function to ask GPT to answer yes/no based on predefined animal
def ask_llm_about_animal(question, predefined_animal):
    prompt = f"Answer the following yes/no question based on the animal: {predefined_animal}.\nQuestion: {question}\nAnswer (Yes/No):"
    
    try:
        # Call OpenAI GPT model for answering the question
        response = client.chat.completions.create(
            model = model,  # "gpt-4" or "gpt-3.5-turbo" or "gpt-4o-mini", depending on access
            messages=[
                #{"role": "system", "content": "You are an assistant that answers yes/no questions about a specific animal."},
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

# User input
user_input = st.text_input("You: ", key="user_input")

# When user submits input
if user_input:
        answer_question = ask_llm_about_animal(user_input, predefined_animal)
        st.session_state["history"].append({"user": user_input, "bot": answer_question})
        st.session_state["input_text"] = ""  # Clear input field

# Display chat history
st.write("### Chat History")
for chat in st.session_state["history"]:
    st.write(f"**You**: {chat['user']}")
    st.write(f"**Bot**: {chat['bot']}")

