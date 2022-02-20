from OpenSea import OpenSea, Collection, Event
import requests

oS = OpenSea()

collection = oS.get_collection("veefriends")
print(collection.totalVolume)
print(collection.ERC721Address)
print(collection.jsonData)
print(collection.floorPrice)
print(collection.sevenDaySales)
collection.load_asset_data()

print(collection.assets[0])