import streamlit as st
import pandas as pd
import numpy as np
import csv

from OpenSea import OpenSea

st.set_page_config(layout="wide")

st.title('NFT Project Analysis Dashboard', )
st.markdown("""---""")
st.header("Floor Price Monitor")

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

with open('collection_names.csv', newline='') as f:
    reader = csv.reader(f)
    collections = list(reader)

oS = OpenSea()
print("{} collections".format(len(collections)))
c = []
for collection in collections:
    c.append(oS.get_collection(collection))
collections = c
for collection in collections:
    print(collection.oneDayChange)
collections.sort(key=lambda x: x.oneDayChange)
for collection in collections:
    print(collection.oneDayChange)

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

with col1:
    #delta metric
    st.metric(label="Bored Ape Yacht Club", value="93.9 ETH", delta="-82.18%")
with col2:
    #delta metric
    st.metric(label="Cryptopunks", value="67.2 ETH", delta="68.06%")
with col3:
    #delta metric
    st.metric(label="Mutant Ape Yacht Club", value="19.7 ETH", delta="-1.74%")
with col4:
    #delta metric
    st.metric(label="These Fucking Nuts", value="93.9 ETH", delta="-82.18%")
with col5:
    #delta metric
    st.metric(label="Cryptopunks", value="67.2 ETH", delta="68.06%")
with col6:
    #delta metric
    st.metric(label="Mutant Ape Yacht Club", value="19.7 ETH", delta="-1.74%")
with col7:
    #delta metric
    st.metric(label="Cryptopunks", value="67.2 ETH", delta="68.06%")
with col8:
    #delta metric
    st.metric(label="Mutant Ape Yacht Club", value="19.7 ETH", delta="-1.74%")

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