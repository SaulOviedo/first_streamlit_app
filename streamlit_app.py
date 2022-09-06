from urllib.error import URLError

import pandas as pd
import requests
import snowflake.connector
import streamlit

s3_url = 'https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt'
my_fruit_list = pd.read_csv(s3_url, index_col='Fruit')

streamlit.title('My Moms\'s New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🍞 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🥚 Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Smoothie 🍇🍓')

fruits_selected = streamlit.multiselect('Pick some fruits', list(my_fruit_list.index), default=['Banana', 'Apple'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show) 

def get_fruityvice(fruit):
    fruityvice_response = requests.get('https://fruityvice.com/api/fruit/' +  fruit)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
    

streamlit.header('Fruityvice Fruit Advice!')
try:
    fruit_choice = streamlit.text_input('What fruit do you want to know about?')
    if not fruit_choice:
        streamlit.error('Please enter a fruit')
    else:
        res = get_fruityvice(fruit_choice)
        streamlit.dataframe(res)

except URLError as e:
    streamlit.error('Please enter a valid fruit')

# Connect to Snowflake
streamlit.header('Fruit Load List contains:')

def get_fruit_load_list():
    with sf.cursor() as cur:
        cur.execute('select * from fruit_load_list')
        return cur.fetchall()
        
if streamlit.button('Get Fruit Load List'):
    sf = snowflake.connector.connect( **streamlit.secrets['snowflake'] )
    fruit_load_list = get_fruit_load_list()
    sf.close()
    streamlit.dataframe(fruit_load_list)

def insert_fruit_load_list(fruit):
    with sf.cursor() as cur:
        cur.execute('insert into fruit_load_list values (%s)', fruit)
        return f'Thanks for adding {fruit} to the Fruit Load List!'

new_fruit = streamlit.text_input('What fruit do you want information about?', 'coconut')
if streamlit.button('Add Fruit to Fruit Load List'):
    sf = snowflake.connector.connect( **streamlit.secrets['snowflake'] )
    streamlit.write(insert_fruit_load_list(new_fruit))
    sf.close()