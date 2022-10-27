import streamlit as sl
import pandas as pd
import requests as req
import snowflake.connector

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')


sl.title("My Mom's New Healthy Diner")

sl.header('Breakfast Favorites')
sl.text('🥣 Omega 3 & Blueberry Oatmeal')
sl.text('🥗 Kale, Spinach & Rocket Smoothie')
sl.text('🐔 Hard-Boiled Free-Range Eggs')
sl.text('🥑🍞 Avocado Toast')

sl.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = sl.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
sl.dataframe(fruits_to_show)
sl.header("Fruityvice Fruit Advice!")
# sl.text(fruityvice_response.json()) # just writes the data to the screen
fruit_choice = sl.text_input('What fruit would you like information about?','Kiwi')
fruityvice_response = req.get("https://fruityvice.com/api/fruit/" + fruit_choice)
sl.write('The user entered ', fruit_choice)

# takes the json version of the response and normalizes it
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# outputs it as a table
sl.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**sl.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("slect * from fruit_load_list")
my_data_row = my_cur.fetchone()
sl.text("The fruit load list contains:")
sl.text(my_data_row)
