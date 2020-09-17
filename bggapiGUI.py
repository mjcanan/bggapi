from tkinter import *
from bggapi import *

'''CURRENTLY CAUSING 429 RESPONSE'''
def callback(selection):
    labels = []
    j = 0

    for i in range(len(c.games)):
        if c.games[i]['name'] == selection:
            g_index = i
    for k in c.games[g_index]:
        mystr = str(k + ": " + str(c.games[g_index][k]))
        mylabel = Label(root, text=mystr)
        labels.append(mylabel)
        labels[j].grid(row=3+j,column=0)
        j += 1


# Loading the Collection
def load_click():
    user_name = u_name.get()
    global c
    c = Collection(user_name)

    if c.load() == 1:
        err_label = Label(root, text="Invalid User")
        err_label.grid(row=2, column=0)
        return
    elif c.load() == 2:
        err_label = Label(root, text="Response 202: Retrying in 3 seconds")
        err_label.grid(row=2, column=0)
        return
    elif c.load() == 3:
        err_label = Label(root, text="User has no available data")
        err_label.grid(row=2, column=0)
        return

    #c.load_price()
    # c.load_price(c.wish_list)
    # c.load_price(c.expansions)
    for game in c.games:
        options.append(game['name'])
    #     games_l = Label(root, text=game['name'])
    #     games_l.pack()
    ugh = StringVar(root)
    ugh.set(options[0])
    opt = OptionMenu(root, ugh, *options,command=callback)
    opt.grid(row=2,column=0)
    load_button.destroy()
    u_name.destroy()




root = Tk()
u_name = Entry(root)
u_name.grid(row=0,column=0)
options = []


load_button = Button(root,text="Enter User Name", command=load_click)
load_button.grid(row=1,column=0)



root.mainloop()
