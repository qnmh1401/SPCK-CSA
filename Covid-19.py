# import streamlit as st
# import pandas as pd
# import numpy as np

# st.title('Uber pickups in NYC')

# DATE_COLUMN = 'date/time'
# DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
#          'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# def load_data(nrows):
#     data = pd.read_csv(DATA_URL, nrows=nrows)
#     lowercase = lambda x: str(x).lower()
#     data.rename(lowercase, axis='columns', inplace=True)
#     data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
#     return data


# # Create a text element and let the reader know the data is loading.
# data_load_state = st.text('Loading data...')
# # Load 10,000 rows of data into the dataframe.
# data = load_data(10000)
# st.text(data)
# # Notify the reader that the data was successfully loaded.
# data_load_state.text(data)


import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
import altair as alt
import numpy as np
def intro():
    

    st.write("# Welcome to Data statistics website !👋")
    st.sidebar.success("Select a chart above.")

    st.markdown(
        """
        This website compiles statistics about total deaths caused by Covid-19

        **👈 Select a chart from the dropdown on the left** to see some data
        ### Where the data come from?
        - Data collected from [Our World in Data](https://ourworldindata.org/coronavirus)
        ### Want to learn more?

        - Check out [Data.gov](https://data.gov)
        - Jump into [Wikipedia.com/covid19](https://en-m-wikipedia-org.translate.goog/wiki/COVID-19?_x_tr_sl=en&_x_tr_tl=vi&_x_tr_hl=vi&_x_tr_pto=tc)
        

        ### See more complex data

        - Use a neural net to [analyze the Udacity Self-driving Car Image
          Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )

def data_frame_demo():
    

    st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")
    st.write(
        """
        This chart show quantity of deaths every day.

(Data source: [Our world in data](https://ourworldindata.org/covid-deaths?country=~CHN).)
"""
    )

    @st.cache_data
    def get_total_death_data():
        # AWS_BUCKET_URL = "https://raw.githubusercontent.com/"
        df = pd.read_csv("totaldeaths.csv")
        return df

    try:
        df = get_total_death_data()

        df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
        df['date'] = df['date'].dt.strftime('%d/%m/%Y')

        df.set_index('date', inplace=True)

        countries = st.multiselect("Choose countries", list(df.columns), ["Vietnam"])
        if not countries:
            st.error("Please select at least one country.")
        else:
            data = df[countries]
            st.write("### Total of deaths in each country", data)

            data = data.T.reset_index()

            data = pd.melt(data, id_vars=["index"]).rename(
                columns={"index": "country", "variable": "date", "value": "Total Deaths By Day"}
            )

            data['date'] = pd.to_datetime(data['date'], format='%d/%m/%Y')

            chart = (
                alt.Chart(data)
                .mark_area(opacity=0.3)
                .encode(
                    x="date:T",
                    y=alt.Y("Total Deaths By Day:Q", stack=None),
                    color="country:N",
                )
            )
            st.altair_chart(chart, use_container_width=True)
            
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**

            Connection error: %s
        """
            % e.reason
        )

# PAGE 2
def line_chart():
    st.markdown(f"# {list(page_names_to_funcs.keys())[1]}")
    st.write(
        """
        This chart shows the statistics of Covid-19 deaths in each country.
        """
    )
    
    @st.cache_data
    def get_total_death_data():
        df = pd.read_csv("totaldeaths.csv")
        return df
    
    df = get_total_death_data()
    
    df['date'] = pd.to_datetime(df['date'])
    
    df.set_index('date', inplace=True)
    
    countries = st.multiselect("Choose countries", list(df.columns), ["Vietnam"])
    
    if not countries:
        st.error("Please select at least one country.")
    else:
        data = df[countries]
        
        data = data.reset_index()
        
        melted_data = pd.melt(data, id_vars=['date'], var_name='Country', value_name='Deaths')
        
        chart = alt.Chart(melted_data).mark_line().encode(
            x='date:T',
            y='Deaths:Q',
            color='Country:N',
            tooltip=['date', 'Country', 'Deaths']
        ).interactive()
        
        st.altair_chart(chart, use_container_width=True)


page_names_to_funcs = {
    "Introduction": intro,
    "Line chart": line_chart,
    #"Mapping Demo": mapping_demo,
    "DataFrame ": data_frame_demo
}

demo_name = st.sidebar.selectbox("Choose a chart", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
