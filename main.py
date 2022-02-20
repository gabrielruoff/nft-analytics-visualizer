from OpenSea import OpenSea, Collection, Event
import requests

oS = OpenSea()

collection = oS.get_collection("one-hour-time-pieces")
print(collection.events[0].total_price)
print(collection.ERC721Address)
print(collection.events[0].jsonData)