# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie.
  """
)
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))

ingredients_list = st.multiselect(
    "Choose upto five ingredinets", 
    my_dataframe,
    max_selections=5,
)

#st.write("You selected:", Ingredients_list)
if ingredients_list:
    ingredients_string = ''
    for i in ingredients_list:
        ingredients_string += i + " "
    st.write(ingredients_string )

name_on_order = st.text_input("Name on the smoothie")
st.write("The name on the smoothie is: ", name_on_order)


my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
         values ('""" + ingredients_string + """','"""+ name_on_order +"""')"""

#st.write(my_insert_stmt)
#st.stop()

time_to_submit = st.button("Submit the Order")

if time_to_submit:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")

