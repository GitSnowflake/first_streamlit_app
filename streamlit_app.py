import streamlit;
import pandas;
import requests;
import snowflake.connector;
from urllib.error import URLError;

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice);
    return fruityvice_response.json();

streamlit.title("My Parents New Healthy Dinner"); 
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt");
my_fruit_list = my_fruit_list.set_index('Fruit');
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Apple']);

fruit_for_advice = [];
fruit_for_advice.append(get_fruityvice_data('Avocado'));
fruit_for_advice.append(get_fruityvice_data('Apple'));

for fruit in fruits_selected:
    fruit_for_advice.append(get_fruityvice_data(fruit));
    
fruits_to_show = my_fruit_list.loc[fruits_selected];
streamlit.dataframe(fruits_to_show);

streamlit.header('🥗FruityVice Fruit Advice:');
   
try:
  #fruit_choice = streamlit.text_input('What fruit would you like information about?');
  if len(fruit_for_advice) == 0:
     streamlit.error('Please select a fruit to get informtaion.');
  else:   
    fruityvice_normalized = pandas.json_normalize(fruit_for_advice);
    streamlit.dataframe(fruityvice_normalized);
    #streamlit.dataframe(get_fruityvice_data(fruit_choice));
except URLError as e:
  streamlit.error();

streamlit.header("The Fruit Load List Contains:");

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
        return my_cur.fetchall();
    
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("INSERT INTO PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST VALUES ('" + new_fruit+ "')");
        return 'Thanks for adding ' + new_fruit
    
if streamlit.button('Get Fruit Load List'): 
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]);
    my_data_row = get_fruit_load_list();
    streamlit.dataframe(my_data_row);
    my_cnx.close();

add_my_fruit = streamlit.text_input('What fruit would you like to add?');
if streamlit.button('Add a fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]);
    back_from_function = insert_row_snowflake(add_my_fruit);
    stremlit.text(back_from_function);
    my_cnx.close();             
