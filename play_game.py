import json
import time
import math
import random
import threading

def main():
    # TODO: allow them to choose from multiple JSON files?
    with open('spooky_mansion.json') as fp:
        game = json.load(fp)
    print_instructions()
    print("You are about to play '{}'! Good luck!".format(game['__metadata__']['title']))
    print("")
    play(game)
start = time.time()
dropped_item = []

transfer = []


def choose_from_list_drop(qtext, options):
    print(qtext)
    for x in range (1, len(options)+1):
        print(x,"-", options[x-1])
    choice = int(input(""))
    if choice >= 0:
        if choice <= len(options):
            print("You dropped", options[choice-1])
            dropped_item.append(options[choice-1])
        else:
            print("That isn't a valid item.")
            dropped_item.append("holder")
    else:
        print("That isn't a valid item.")
        dropped_item.append("holder")


   

def play(rooms):
    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = rooms['__metadata__']['start']
    # The things the player has collected.
    stuff = ['Dead Cell Phone']
    while True:
        # Figure out what room we're in -- current_place is a name.
        here = rooms[current_place]
        # Print the description.
        print(here["description"])

        if len(here["items"]) != 0:
            print("There is a",here["items"])

        
        # TODO: print any available items in the room...
        # e.g., There is a Mansion Key.

        # Is this a game-over?
        if here.get("ends_game", False):
            break

        # Allow the user to choose an exit:
        usable_exits = find_visable_exits(here)
        # Print out numbers for them to choose:
        for i, exit in enumerate(usable_exits):
            print("  {}. {}".format(i+1, exit['description']))

        # See what they typed:
        action = input("> ").lower().strip()

        # If they type any variant of quit; exit the game.
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break
        
        
        if action == "help":
            print_instructions()
            continue
        
        if action == "stuff":
            if len(stuff) == 0:
                print("You have nothing")
                continue
            else:
                print("You have:",stuff)
                continue
        
        if action == "take":
            if len(here["items"]) == 0:
                print("there is nothing to take")
                continue
            else:
                if here["items"] in stuff:
                    print("you already have", here["items"])
                    continue
                else:
                    for x in here["items"]:
                        stuff.append(x)
                    print("you put", here["items"], "in your bag")
                    here["items"].clear()
                    continue
                    
        if action == "drop":
            choose_from_list_drop("Which item would you like to drop",stuff)
            if dropped_item[0] in stuff:
                here["items"].append(dropped_item[0])
                stuff.remove(dropped_item[0])
                dropped_item.clear()
                continue
            else:
                dropped_item.clear()
                continue
                    
        
        if action == "time":
            current = time.time()
            print("You have been playing for", math.floor((current - start)/60), "minutes, and", (round(current - start)) - 60*(math.floor((current - start)/60)), "seconds")
            continue
        
        end = time.time()
        
        if action == "when":
            print(end - start)
            
        all_rooms = ["entranceHall", "basement", "attic", "attic2", "balcony", "kitchen", "dumbwaiter", "secretRoom", "crypt"]
            
        def cat():
            threading.Timer(10.0, cat).start()
            cat_travel = []
            cat_travel.append(all_rooms[random.randint(0,8)])
            if cat_travel[0] == here['name']:
                print("A little black cat enters the room")
                cat_travel.clear()
            else:
                cat_travel.clear()
                
        
        if action == "cat":
            cat()
            continue

        all_rooms_easteregg = ["entranceHall", "basement", "attic", "balcony", "kitchen", "dumbwaiter", "moon"]


        if here['name'] == "teleporter":
            random_room = []
            random_room.append(all_rooms_easteregg[random.randint(0,6)])
            current_place = random_room[0]
            print("ZAP")
            print("you have been randomly teleported throughout the mansion")
            random_room.clear()
            continue
        

        # TODO: if they type "stuff", print any items they have (check the stuff list!)
        # TODO: if they type "take", grab any items in the room.
        # TODO: if they type "search", or "find", look through any exits in the room that might be hidden, and make them not hidden anymore!
        
        # Try to turn their action into an exit, by number.
        try:
            num = int(action) - 1
            selected = usable_exits[num]
            current_place = selected['destination']
            

        except:
            print("I don't understand '{}'...".format(action))
        
    print("")
    print("")
    print("=== GAME OVER ===")

def find_visable_exits(room):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
    That means the exits must not be hidden, and if they require a key, the player has it.

    RETURNS
     - a list of exits that are visible (not hidden).
    """
    usable = []
    for exit in room['exits']:
        if exit.get("hidden", False):
            continue
        usable.append(exit)
    return usable

def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'help' to see instructions again.")
    print(" - Type 'time' to see how long you have been playing for.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print("***Type 'cat' to release the cat around the mansion***")
    print("=== Instructions ===")
if __name__ == '__main__':
    main()
