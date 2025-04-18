# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie.
  """
)

name_on_order = st.text_input("Name on the smoothie")
st.write("The name on the smoothie is: ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'), col('search_on'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()    
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

ingredients_list = st.multiselect(
    "Choose upto five ingredinets", 
    my_dataframe,
    max_selections=5,
)

#st.write("You selected:", Ingredients_list)
if ingredients_list:
    ingredients_string = ''
    for i in ingredients_list:        # here 'i' is 'fruit_chosen'
        ingredients_string += i + " "
      
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == i, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', i,' is ', search_on, '.')
      
        st.subheader( i + 'Nutrition_information' )
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + i)
        st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    st.write(ingredients_string )



my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
         values ('""" + ingredients_string + """','"""+ name_on_order +"""')"""

#st.write(my_insert_stmt)
#st.stop()

time_to_submit = st.button("Submit the Order")

if time_to_submit:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
