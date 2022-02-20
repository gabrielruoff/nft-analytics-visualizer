from gc import collect
from matplotlib import image
from matplotlib.pyplot import bar
import streamlit as st
import pandas as pd
import numpy as np
import csv
from millify import millify
import re
from OpenSea import OpenSea, Collection, Event
import requests
import altair as alt


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
    st.metric(label=headerCollection_7.name, value=str(round(headerCollection_7.floorPrice, 3)) + " ETH", delta=str(round((100*headerCollection_7.oneDayChange), 2)) + "%")
with col8:
    #delta metric
    st.image(headerCollection_8.image)
    st.metric(label=headerCollection_8.name, value=str(round(headerCollection_8.floorPrice, 3)) + " ETH", delta=str(round((100*headerCollection_8.oneDayChange), 2)) + "%")

st.header("Collection Data")

collectionDF=pd.read_csv(r'collection_names.csv')
collection_list=collectionDF.drop_duplicates().values.tolist()
collection_list = [x[0] for x in collection_list]
#print(collection_list)
realNameList = []
#for name in collection_list:
    #print(name)
 #   tempCollection = oS.get_collection(name)
    #print(tempCollection)
  #  realNameList.append(tempCollection) """

graphOption = st.selectbox('Type to search and select a collection to visualize', collection_list, help="Collection data compiled from OpenSea", index = 358) 
print(graphOption)
graphCollection = oS.get_collection(graphOption)
#print(graphCollection.name)



# Create a text element and let the reader know the data is loading.
#data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.

#data_load_state.text("Done! (using st.cache)")
#betaCol1, betaCol2 = st.columns(2)
#betaCol2.header("Collection Data")
#betaCol1.image(graphCollection.image)
st.subheader(graphCollection.name)
st.markdown("""---""")

sub1, sub2, sub3, sub4, sub5, sub6, sub65= st.columns(7)
#sub1.image(graphCollection.image)
sub1.metric("Total Supply", millify(graphCollection.totalSupply))
sub2.metric("Total Sales", millify(graphCollection.totalSales))
sub3.metric("Total Volume", round(graphCollection.totalVolume),3)


sub4.header("               |")
sub5.metric("1 Day Sales", graphCollection.oneDaySales)
sub6.metric("1 Day Average Price", str(round(graphCollection.oneDayAvgPrice, 2)) + " ETH", delta=str(round((100*graphCollection.oneDayChange), 2)) + "%")
sub65.metric("1 Day Volume", round(graphCollection.oneDayVolume, 3))
st.markdown("""---""")

sub7, sub8, sub9, sub10, sub11, sub12, sub13= st.columns(7)
st.markdown("""---""")

sub7.metric("7 Day Sales", graphCollection.sevenDaySales)
sub8.metric("7 Day Average Price", str(round(graphCollection.sevenDayAvgPrice, 2)) + " ETH", delta=str(round((100*graphCollection.sevenDayChange), 2)) + "%")
sub9.metric("7 Day Volume", round(graphCollection.sevenDayVolume, 3))
sub10.header("|")
sub11.metric("30 Day Sales", graphCollection.thirtyDaySales)
sub12.metric("30 Day Average Price", str(round(graphCollection.thirtyDayAvgPrice, 2)) + " ETH", delta=str(round((100*graphCollection.thirtyDayChange), 2)) + "%")
sub13.metric("30 Day Volume", round(graphCollection.thirtyDayVolume, 3))

st.subheader("Price Activity")
graphCollection.load_event_data()
eventList = []
for event in graphCollection.events:
    eventList.append(event.total_price)
print(eventList)
line_chart_data = pd.DataFrame({'Dates': eventList, 'Price (ETH)':graphCollection.event_dates})

chart = (
    alt.Chart(line_chart_data).mark_line().encode(
        x = 'Dates',
        y = 'Price (ETH)'
    )
)
st.altair_chart(chart,use_container_width=True)