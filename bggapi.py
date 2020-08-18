import requests
import xml.etree.ElementTree as ET
import sys

wrongName = True
while wrongName:
    try:
        user = input("Enter your BBG Username: ")
        response = requests.get("https://api.geekdo.com/xmlapi2/collection?username=" + user + "&own=1")
        tree = ET.fromstring(response.content)
        wrongName = False
    except:
        print("Whoops!  Something went wrong.  Please try again later.")
        sys.exit()

    if not tree.attrib:
        for errors in tree.findall('error'):
            e = errors.find('message').text
        print(e)
        wrongName = True

i = 1
for item in tree.findall('item'):
    name = item.find('name').text
    print(f"{i}: {name}")
    i = i + 1
print("--------------------------------")
print(f"Total games: {i-1}")

# TODO: Allow for more specific parsing (previously owned, on wish list) and sorting
# TODO: Add GUI (tkinter)
# TODO: Better Error Handling
# TODO: Organize code into functions
# TODO: Comment