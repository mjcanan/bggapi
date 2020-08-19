import sys
import untangle

wrongName = True
while wrongName:
    try:
        user = input("Enter your BBG Username: ")
        apiURL = str("https://api.geekdo.com/xmlapi2/collection?username=" + user + "&own=1")
        obj = untangle.parse(apiURL)
        wrongName = False
    except Exception as err:
        print(err)
        sys.exit()


# TODO: loop to get objects parsed
print("--------------------------------")

# TODO: Allow for more specific parsing (previously owned, on wish list) and sorting
# TODO: Add GUI (tkinter)
# TODO: Better Error Handling
# TODO: Create game objects that are populated from the xml and stored in an array
# TODO: Comment

# untangle documentation:
# https://readthedocs.org/projects/untangle/downloads/pdf/latest/#:~:text=untangle%20is%20a%20tiny%20Python,available%20under%20the%20MIT%20license.&text=untangle.,which%20represents%20the%20given%20document.