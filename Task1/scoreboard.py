import streamlit as st
import pandas as pd
import numpy as np
from itertools import chain

#stylize page
st.set_page_config(layout="wide")
st.title("Stats")
st.header("Scoreboard")
col1, col2 = st.columns(2)

number = "0"

#read in the data collected during the games from the csv to later create two dataframes 
#(one for quantity and one for quality of guesses)
scores = pd.DataFrame({'Emily': [np.random.randint(1,15), np.random.rand(1,15)], 'Lena': [np.random.randint(1,15), np.random.rand(1,15)], 'Luna':[np.random.randint(1,15), np.random.rand(1,15)]}, index=["quantity","quality"])

#create a dataframe for quantity of guesses
quantity = pd.DataFrame(scores['quantity'])
quantity = quantity.sort_values(['quantity'], axis = 0)

#display the quantity scoreboard
with col1:
    st.subheader("Scoreboard by quantity of guesses")
    st.dataframe(quantity)


def flatten_chain(matrix):
    """a function to flatten any n-dimensional matrix to a list"""
    return list(chain.from_iterable(matrix))

#create a dataframe for the quality of guesses
quality =  scores['quality']
avg_qual = {}
#get the average quality of guesses per person
for index, value in quality.items():
    value = flatten_chain(value)
    avg_qual[index] = sum(value) / len(value)
average_quality = pd.DataFrame(avg_qual)
average_quality.sort_values(['quality'], ascending = False, axis= 0)

#display the scoreboard for average quality of guesses
with col2:
    st.subheader("Scoreboard by quality of guesses")
    st.dataframe(average_quality)

#section for further statistics 
st.header("Further Statistics")
st.text("Number of Games played: " + number)

st.text("Average number of guesses: ")

print(quantity)
print(average_quality)

st.subheader("Number of guesses per game")
#st.bar_chart(scores)

st.subheader("Average quality of guesses per game")
#st.bar_chart(average_quality, x = average_quality.columns, y = average_quality["quality"])


