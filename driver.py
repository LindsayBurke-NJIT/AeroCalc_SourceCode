############################################################################################
# Author: Lindsay Burke
# Date: 7/29/2023
# Description:  This program was built for the NJIT Flylanders SAE Aero Design Team.
#               It is a compilation of calculators and tools for gathering information about
#               our RC plane design in various crucial aspects-- wing/tail, electronics,
#               fuselage, and landing gear.
############################################################################################

from tkinter import *
from tkinter import ttk
import sys
import support_functions.general_window_functions as general
from support_functions.images import addImg

#import for splash screen with pyinstaller whenever exe is run
if getattr(sys, 'frozen', False):
    import pyi_splash

#root config
root = Tk()
canvas = Canvas()

root.title("NJIT Flylanders™ AeroCalc")
windowWidth = 640
windowHeight=630
root.geometry(f'{windowWidth}x{windowHeight}')
root.resizable(True, True)

# Configure grid weights for responsive layout
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=0)  # Button sidebar - fixed width
root.columnconfigure(1, weight=1)  # Tab content - expandable

try:
    imgPath = addImg("aeroLogo.png")
    photo = PhotoImage(file = imgPath)
    root.iconphoto(False, photo)
except:
    pass

#Initialize tab style
myTheme = ttk.Style()
myTheme.theme_create( "myTheme", settings={
        "TNotebook": {"configure": {"tabmargins": [0, 4, 0, 0]}},
        "TNotebook.Tab": {"configure": {"padding": [5, 5]}}
        })
myTheme.theme_use("myTheme")
tabControl = ttk.Notebook(root)
tabControl.grid(row=0, column=1, sticky='nsew')
tabControl.rowconfigure(0, weight=1)
tabControl.columnconfigure(0, weight=1)

#Change color/font styles here
colorSelection= "lightgray"
fontName = "Roboto"

#Buttons setup
buttons = Frame(root, width=100, height=1000, bg="lightgray")
buttons.grid(row=0, column=0, sticky='ns')
buttons.grid_propagate(False)  # Keep fixed width
buttonColor = "#b40707"
buttonText = "Roboto 12 bold"
reliefStyle="solid"
buttonTextColor = "black"
buttonHeight = 4
buttonList = {}

def main():
    windowObj = general.GeneralWindowFunctions(tabControl, (windowWidth, windowHeight), colorSelection,
                                               fontName, buttonList, buttonTextColor,
                                               buttonColor, buttonHeight, buttonText, reliefStyle)
    #                      (button name, function, text to display, Tk Frame)
    windowObj.createButton("Home", windowObj.homeActivate, "Home", buttons)
    windowObj.createButton("Wing", windowObj.wingActivate, "Wing", buttons)
    windowObj.createButton("Tail", windowObj.tailActivate, "Tail", buttons)
    windowObj.createButton("Electronics", windowObj.electronicsActivate, "Electronics", buttons)
    windowObj.createButton("Landing Gear", windowObj.landgearActivate, "Landing\nGear", buttons)
    windowObj.createButton("Fuselage", windowObj.fuselageActivate, "Fuselage", buttons)
    windowObj.createButton("Misc", windowObj.miscActivate, "Misc.", buttons)

    windowObj.homeActivate() #start with home page displaying to user
    if getattr(sys, 'frozen', False):
        pyi_splash.close()
    root.mainloop()

if __name__ == "__main__":
    main()