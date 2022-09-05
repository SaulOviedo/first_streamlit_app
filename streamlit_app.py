import streamlit
import pandas as pd

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