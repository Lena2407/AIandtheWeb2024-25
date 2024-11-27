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


def flatten_chain(matrix):
    """a function to flatten any n-dimensional matrix to a list"""
    return list(chain.from_iterable(matrix))

#read in the data collected during the games from the csv to later create multiple DataFrames 
scores = pd.read_csv('statistics.csv', index_col=0)

#create a DataFrame for quantity of guesses, sort for the scoreboard
quantity = pd.DataFrame(scores['quantity'])
quantity = quantity.sort_values(['quantity'], axis = 0)
guesscount = quantity['quantity'].tolist()

#display the quantity scoreboard
with col1:
    st.subheader("Scoreboard by quantity of guesses")
    st.dataframe(quantity)


#create a dataframe for the quality of guesses
quality = scores['quality'].apply(ast.literal_eval)
helper = {}
avg_qual = {}
#get the average quality of guesses per person
#helper helps for users that played multiple games under the same username
for index, value in quality.items():
    if index in helper.keys():
        helper[index].append(value)
    else: 
        helper[index] = [value]
for index, value in helper.items():
    value = flatten_chain(value)
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

# calculates how many times each word was guessed and sorts them by wordcount
guesses = scores['guesses'].apply(ast.literal_eval)
wordcount = {}
for index, words in guesses.items():
    for word in words: 
        if word in wordcount.keys(): 
            wordcount[word] = int(wordcount[word]) + 1
        else: 
            wordcount[word] = 1
most_guessed = max(wordcount, key=wordcount.get)
words = pd.Series(wordcount).sort_values(ascending=False)

st.text("Most guessed word: " + str(most_guessed))


# section with bar charts for top 10 most used words, users with most guesses and number of guesses per game

st.subheader("Top 10: Most guessed words")
st.bar_chart(words.head(10), color = "#9621dd")

st.subheader("Users with most guesses")
st.bar_chart(quantity.sort_values(['quantity'], ascending=False).head(10), x_label = "Usernames", color = "#9621dd")

st.subheader("Number of guesses per game")
st.bar_chart(quantity, x_label = "Usernames", color = "#9621dd")


