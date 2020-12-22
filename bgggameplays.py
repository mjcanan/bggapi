import bggapi

collection = bggapi.Collection('flakcanon')
collection.load_plays()
print(collection)