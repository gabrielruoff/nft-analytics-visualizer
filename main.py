import csv
import time

from OpenSea import OpenSea, Collection, Event
import requests

oS = OpenSea()

# collection = oS.get_collection("veefriends")
# print(collection.events[0].total_price)
# print(collection.ERC721Address)
# print(collection.jsonData)
# print(collection.floorPrice)
# print(collection.sevenDaySales)
# print(collection.assets[0].name)

with open('collection_names.csv', newline='') as f:
    reader = csv.reader(f)
    # for i in range(1294):
    #     next(reader)
    collections = list(reader)

print("{} collections".format(len(collections)))
c = []
i=0
for collection in collections:

    print(collection[0])
    c = oS.get_collection(collection[0], path='collectiondata/')
    print(c.oneDayChange)
    i += 1
    # print(c.jsonData)
    # try:
    #     c.export_json_data('collectiondata/')
    # except Exception:
    #     pass
    # time.sleep(0.1)
# collections = c
# for collection in collections:
#     print(collection.oneDayChange)
# collections.sort(key=lambda x: x.oneDayChange)
# for collection in collections:
#     print(collection.oneDayChange)

f.close()
print(i)