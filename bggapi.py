import requests
import xml.etree.ElementTree as ET
import sys


def printoutput(tree):
    i = 1
    print("\n--------------------------------")
    for item in tree.findall('item'):
        name = item.find('name').text
        print(f"{i}: {name}")
        i = i + 1
    print("--------------------------------")
    print(f"Total games: {i - 1}")


def main():
    wrongName = True
    option = -1

    while wrongName:
        try:
            user = input("Enter your BBG Username: ")

            # TODO: Option Function

            while option not in range(1, 3):
                try:
                    option = int(input("Select Option: Own (1), Wishlist (2): "))
                except ValueError as err:
                    print(err)
                if option not in range(1, 3):
                    print("Usage: Enter 1 for 'Own', Enter 2 for 'Wishlist'")

            if option == 1:
                setting = "&own=1"
            else:
                setting = "&wishlist=1"

            apiURL = str("https://api.geekdo.com/xmlapi2/collection?username=" + user + setting)
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

    printoutput(tree)


main()

# TODO: Allow for more specific parsing (previously owned, on wish list) and sorting
# TODO: Add GUI (tkinter)
# TODO: Better Error Handling
# TODO: Organize code into functions
# TODO: Comment
