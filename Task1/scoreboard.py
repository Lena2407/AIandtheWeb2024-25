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

def flatten_chain(matrix):
    return list(chain.from_iterable(matrix))



scores = pd.DataFrame({'Emily': [np.random.randint(1,15), np.random.rand(1,15)], 'Lena': [np.random.randint(1,15), np.random.rand(1,15)], 'Luna':[np.random.randint(1,15), np.random.rand(1,15)]}, index=["quantity","quality"])
quantity = pd.DataFrame(scores['quantity'])
quantity = quantity.sort_values(['quantity'], axis = 0)
with col1:
    st.subheader("Scoreboard by quantity of guesses")
    st.dataframe(quantity)


quality =  scores['quality']
avg_qual = {}
for index, value in quality.items():
    value = flatten_chain(value)
    avg_qual[index] = sum(value) / len(value)
average_quality = pd.DataFrame(avg_qual)
print(average_quality)
average_quality.sort_values(['quality'], ascending = False, axis= 0)

with col2:
    st.subheader("Scoreboard by quality of guesses")
    st.dataframe(average_quality)

## for score: +1 per guess for quantity, save quality of each guess and give mean quality back at the end
st.header("Further Statistics")
st.text("Number of Games played: " + number)

st.text("Average number of guesses: ")

print(quantity)
print(average_quality)

st.subheader("Number of guesses per game")
#st.bar_chart(scores)

st.subheader("Average quality of guesses per game")
#st.bar_chart(average_quality, x = average_quality.columns, y = average_quality["quality"])


