from OpenSea import OpenSea, Collection, Event
import requests

# oS = OpenSea()
# collections = oS.get_collections(limit=20)
# print(collections['collections'][0])
# c = []
# for collection in collections['collections']:
#     if collection['stats']['total_supply'] != 0.0:
#         c.append(collection)
# collections = c
#
# print(collections)
# print(len(collections))
headers = {"Accept": "application/json"}
response = requests.request("GET", "https://opensea.io/rankings", headers=headers)
print(response.text)