from gc import collect
from matplotlib import image
import streamlit as st
import pandas as pd
import numpy as np
import csv
from millify import millify
from OpenSea import OpenSea, Collection, Event
import requests


#page initilization
st.set_page_config(layout="wide")
oS = OpenSea()
headerCollection_1 = oS.get_collection("boredapeyachtclub")
headerCollection_2 = oS.get_collection("azuki")
headerCollection_3 = oS.get_collection("meebits")
headerCollection_4 = oS.get_collection("genesis-creepz")
headerCollection_5 = oS.get_collection("deadfellaz")
headerCollection_6 = oS.get_collection("cyberkongz")
headerCollection_7 = oS.get_collection("candy-hunters")
headerCollection_8 = oS.get_collection("sorare")

st.title('NFT Project Analysis Dashboard', )
st.markdown("""---""")
st.header("Floor Price Monitor")

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

with col1:
    #delta metric
    st.image(headerCollection_1.image)
    st.metric(label=headerCollection_1.name, value=str(headerCollection_1.floorPrice) + " ETH", delta=str(round((100*headerCollection_1.oneDayChange), 2)) + "%")
with col2:
    #delta metric
    st.image(headerCollection_2.image)
    st.metric(label=headerCollection_2.name, value=str(headerCollection_2.floorPrice) + " ETH", delta=str(round((100*headerCollection_2.oneDayChange), 2)) + "%")
with col3:
    #delta metric
    st.image(headerCollection_3.image)
    st.metric(label=headerCollection_3.name, value=str(headerCollection_3.floorPrice) + " ETH", delta=str(round((100*headerCollection_3.oneDayChange), 2)) + "%")
with col4:
    #delta metric
    st.image(headerCollection_4.image)
    st.metric(label=headerCollection_4.name, value=str(headerCollection_4.floorPrice) + " ETH", delta=str(round((100*headerCollection_4.oneDayChange), 2)) + "%")
with col5:
    #delta metric
    st.image(headerCollection_5.image)
    st.metric(label=headerCollection_5.name, value=str(headerCollection_5.floorPrice) + " ETH", delta=str(round((100*headerCollection_5.oneDayChange), 2)) + "%")
with col6:
    #delta metric
    st.image(headerCollection_6.image)
    st.metric(label=headerCollection_6.name, value=str(headerCollection_6.floorPrice) + " ETH", delta=str(round((100*headerCollection_6.oneDayChange), 2)) + "%")
with col7:
    #delta metric
    st.image(headerCollection_7.image)
    st.metric(label=headerCollection_7.name, value=str(headerCollection_7.floorPrice) + " ETH", delta=str(round((100*headerCollection_7.oneDayChange), 2)) + "%")
with col8:
    #delta metric
    st.image(headerCollection_8.image)
    st.metric(label=headerCollection_8.name, value=str(headerCollection_8.floorPrice) + " ETH", delta=str(round((100*headerCollection_8.oneDayChange), 2)) + "%")

collectionDF=pd.read_csv(r'collection_names.csv')
collection_list=collectionDF.drop_duplicates().values

graphOption = st.selectbox('Select a collection to visualize', collection_list) 


@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)
st.subheader('Number of pickups by hour')

hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

st.bar_chart(hist_values)
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h



filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)