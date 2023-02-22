import streamlit;
import pandas;
import requests;
import snowflake.connector;
from urllib.error import URLError;

streamlit.title("My Parents New Healthy Dinner"); 

fruityvice_response1 = requests.get("https://fruityvice.com/api/fruit/Apple");
fruityvice_response2 = requests.get("https://fruityvice.com/api/fruit/Orange");
streamlit.text(fruityvice_response1.json()); # {'genus': 'Malus', 'name': 'Apple', 'id': 6, 'family': 'Rosaceae', 'order': 'Rosales', 'nutritions': {'carbohydrates': 11.4, 'protein': 0.3, 'fat': 0.4, 'calories': 52, 'sugar': 10.3}}
streamlit.text(fruityvice_response2.json()); # {'genus': 'Citrus', 'name': 'Orange', 'id': 2, 'family': 'Rutaceae', 'order': 'Sapindales', 'nutritions': {'carbohydrates': 8.3, 'protein': 1, 'fat': 0.2, 'calories': 43, 'sugar': 8.2}}
full_response = f'{[{'genus': 'Malus', 'name': 'Apple', 'id': 6, 'family': 'Rosaceae', 'order': 'Rosales', 'nutritions': {'carbohydrates': 11.4, 'protein': 0.3, 'fat': 0.4, 'calories': 52, 'sugar': 10.3}}, {'genus': 'Citrus', 'name': 'Orange', 'id': 2, 'family': 'Rutaceae', 'order': 'Sapindales', 'nutritions': {'carbohydrates': 8.3, 'protein': 1, 'fat': 0.2, 'calories': 43, 'sugar': 8.2}}]}';
streamlit.text(full_response);
fruityvice_normalized = pandas.json_normalize(full_response);
streamlit.text(fruityvice_normalized);

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt");
my_fruit_list = my_fruit_list.set_index('Fruit');
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries']);
fruits_to_show = my_fruit_list.loc[fruits_selected];
streamlit.dataframe(fruits_to_show);

streamlit.header('🥗FruityVice Fruit Advice:');
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice);
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json());
    return fruityvice_normalized;
    
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?');
  if not fruit_choice:
     streamlit.error('Please select a fruit to get informtaion.');
  else:    
    streamlit.dataframe(get_fruityvice_data(fruit_choice));
except URLError as e:
  streamlit.error();

streamlit.header("The Fruit Load List Contains:");


def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
        return my_cur.fetchall();
    
if streamlit.button('Get Fruit Load List'): 
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]);
    my_data_row = get_fruit_load_list();
    streamlit.dataframe(my_data_row);
    
    
    
    
streamlit.stop();
fruit_added = streamlit.text_input('What fruit would you like to add?','');
my_cur.execute("INSERT INTO FRUIT_LOAD_LIST() VALUES ()");
streamlit.write(fruit_added, ' added succeffully!');
