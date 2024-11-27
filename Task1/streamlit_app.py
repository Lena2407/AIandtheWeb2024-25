import streamlit as st

pg = st.navigation([st.Page("guessing_game_with_chatbot.py", title="Guessing Game", ), st.Page("scoreboard.py", title = "Statistics")])
pg.run()