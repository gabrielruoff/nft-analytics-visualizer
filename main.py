from OpenSea import OpenSea, Collection, Event
import requests

oS = OpenSea()

collections = oS.get_collections(limit=300)
for collection in collections:
    print(collection.jsonData)