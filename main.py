from OpenSea import OpenSea, Collection, Event
import requests

oS = OpenSea()

collection = oS.get_collection("veefriends")
print(collection.events[0].total_price)
print(collection.ERC721Address)
print(collection.jsonData)
print(collection.floorPrice)
print(collection.sevenDaySales)