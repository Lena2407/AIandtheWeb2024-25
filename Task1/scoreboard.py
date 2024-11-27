import streamlit as st
import pandas as pd
import numpy as np
from itertools import chain
import ast
import statistics

#stylize page
st.set_page_config(layout="wide")

#set page title and header
st.title("Stats")
st.header("Scoreboard")
col1, col2 = st.columns(2)


#read in the data collected during the games from the csv to later create two dataframes 
#(one for quantity and one for quality of guesses)
scores = pd.read_csv('statistics.csv', index_col=0)

#create a dataframe for quantity of guesses
quantity = pd.DataFrame(scores['quantity'])
quantity = quantity.sort_values(['quantity'], axis = 0)
guesscount = quantity['quantity'].tolist()

#display the quantity scoreboard
with col1:
    st.subheader("Scoreboard by quantity of guesses")
    st.dataframe(quantity)


def flatten_chain(matrix):
    """a function to flatten any n-dimensional matrix to a list"""
    return list(chain.from_iterable(matrix))

#create a dataframe for the quality of guesses
quality = scores['quality'].apply(ast.literal_eval)
avg_qual = {}
#get the average quality of guesses per person
for index, value in quality.items():
    avg_qual[index] = statistics.fmean(value)
average_quality = pd.DataFrame(avg_qual, index=['quality'])
average_quality= average_quality.sort_values(['quality'], ascending = False, axis= 1)

#display the scoreboard for average quality of guesses
with col2:
    st.subheader("Scoreboard by quality of guesses")
    st.dataframe(average_quality.T)

#section for further statistics 
st.header("Further Statistics")
st.text("Number of Games played: " + str(scores.shape[0]))

st.text("Average number of guesses: " + str(statistics.fmean(guesscount)))

guesses = scores['guesses'].apply(ast.literal_eval)
print(guesses)
wordcount = {}
for index, words in guesses.items():
    print(words)
    for word in words: 
        if word in wordcount.keys(): 
            wordcount[word] = int(wordcount[word]) + 1
        else: 
            wordcount[word] = 1
most_guessed = max(wordcount, key=wordcount.get)

st.text("Most guessed word: " + str(most_guessed))

#print(quantity)
#print(average_quality)

st.subheader("Number of guesses per game")
st.bar_chart(quantity, x_label = "Usernames", color = "#9621dd")

st.subheader("Average quality of guesses per game")
st.bar_chart(average_quality.T, x_label = "Usernames", color = "#9621dd")

st.subheader("Most guessed words")
st.bar_chart(wordcount, color = "#9621dd")


