import sys
import untangle

wrongName = True

def printOutput(obj):
    totalplays = 0

    print('Name                               Number of Plays')
    print('-' * 50)

    for x in range(len(obj.items)):
        nameformat = [" "] * 50
        y = 0
        numplays = obj.items.item[x].numplays.cdata
        totalplays = totalplays + int(numplays)
        for char in obj.items.item[x].name.cdata:
            nameformat[y] = char
            y = y + 1
        nameformat[-1] = numplays
        print("".join(nameformat))

    print('-' * 50)
    print('Total Games: %d' % len(obj.items) + ' ' * 20 + 'Total Plays: %d' % totalplays)

while wrongName:
    try:
        user = input("Enter your BBG Username: ")
        apiURL = str("https://api.geekdo.com/xmlapi2/collection?username=" + user + "&own=1")
        objGames = untangle.parse(apiURL)
        wrongName = False
    except Exception as err:
        print(err)
        sys.exit()

printOutput(objGames)


# TODO: Allow for more specific parsing (previously owned, on wish list) and sorting
# TODO: Add GUI (tkinter)
# TODO: Better Error Handling
# TODO: Create game objects that are populated from the xml and stored in an array

# untangle documentation:
# https://readthedocs.org/projects/untangle/downloads/pdf/latest/#:~:text=untangle%20is%20a%20tiny%20Python,available%20under%20the%20MIT%20license.&text=untangle.,which%20represents%20the%20given%20document.