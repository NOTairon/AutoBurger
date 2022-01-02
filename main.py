print("Initializing...")
from userInput import execMenu, init, getTopOrderCoords, getBotOrderCoords, getMenuCoords, getRepeats
from classifier import getOrderImg, getOrderItems, removeText, classifyShape
import os, time


if __name__ == "__main__":
    #init()
    topCoords= getTopOrderCoords()
    botCoords = getBotOrderCoords()
    menu_coords = getMenuCoords()
    repeats = getRepeats()
    order_region = (topCoords[0],topCoords[1],botCoords[0],botCoords[1])
    while 1: # Main Automation loop
        orders = []
        cnt = 0 
        item_coords = 0
        item_corners = [[] for _ in range(repeats)]
        for i in range(repeats):
            img = getOrderImg(order_region) # Get the order
            img = removeText(img) # Remove any text
            cnt, item_coords, corners = getOrderItems(img) # Get order items
            counter = 0
            while True:
                if len(item_corners[counter]) != 0:
                    counter += 1
                else:
                    break
            item_corners[counter] = corners
        corners = []
        try:
            for i in range(len(item_corners[0])):
                tmp_sum = 0
                for j in range(repeats):
                    tmp_sum += item_corners[j][i]
                corners.append(tmp_sum // repeats) # get the average

            print("There is {} item(s)".format(cnt))
            print(item_coords)
        except:
            print("Scanning took too long, if this happened on the first customer, don't worry, but if this message takes too long then try reducing the amount of repeats.")


        if cnt == 3: # orders of three always have the following items.
            orders.append("cola")
            orders.append("fries")
            # remove the items from the coords list since we don't need to scan them.
            item_coords.pop(2)
            item_coords.pop(1)
            corners.pop(2)
            corners.pop(1)
            print("Cola and fries automatically added.")
            print("Burger has {} corners".format(corners[0]))
            orders.append(classifyShape(corners[0],"main"))
        
        elif cnt == 2:
            print("Burger has {} corners".format(corners[0]))
            orders.append(classifyShape(corners[0],"main"))
 
            print("Side has {} corners".format(corners[1]))
            orders.append(classifyShape(corners[1],"side"))

        elif cnt == 1:
            print("Burger has {} corners".format(corners[0]))
            orders.append(classifyShape(corners[0],"main"))
 
        else:
            print("No customer")
        print(orders)
        time.sleep(0.5)
        execMenu(orders,menu_coords)
        time.sleep(5)
