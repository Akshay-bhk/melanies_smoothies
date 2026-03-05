# Import python packages
import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw:  CUSTOMIZE YOUR SMOOTHIE  :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

name_on_order = st.text_input("Name on smoothie:")
st.write("The name on your smoothie will be :", name_on_order)

# Snowflake connection
cnx = st.connection('snowflake')
session = cnx.session()

# Get fruit list from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()

# Convert column to list
fruit_list = my_dataframe["FRUIT_NAME"].tolist()

# Multiselect
ingredients_list = st.multiselect(
    "Choose upto 5 ingredients:",
    fruit_list
)

if ingredients_list:

    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "

    my_insert_stmt = """INSERT INTO smoothies.public.orders (ingredients, name_on_order)
VALUES ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


# -------- SmoothieFroot Nutrition Section --------
st.subheader("SmoothieFroot Nutrition Information")

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit")

if smoothiefroot_response.status_code == 200:

    fruit_json = smoothiefroot_response.json()

    fruit_df = pd.DataFrame(fruit_json)

    st.dataframe(fruit_df, use_container_width=True)
