import requests
import xml.etree.ElementTree as ET
import sys
#import untangle

wrongName = True
while wrongName:
    try:
        user = input("Enter your BBG Username: ")
        apiURL = str("https://api.geekdo.com/xmlapi2/collection?username=" + user + "&own=1")
        response = requests.get(apiURL)
        tree = ET.fromstring(response.content)
        wrongName = False
    except Exception as err:
        print(err)
        sys.exit()

    if not tree.attrib:
        for errors in tree.findall('error'):
            e = errors.find('message').text
        print(e)
        wrongName = True
# playing with untangle
#    obj = untangle.parse(apiURL)

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