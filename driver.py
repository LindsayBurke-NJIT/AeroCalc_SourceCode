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
import sys, os
import support_functions.tailTab1_support_functions as tailTab1
import support_functions.elecTab1_support_functions as elecTab1
import support_functions.homepage_support_functions as homepage
import support_functions.wingTab1_support_functions as wingTab1
import support_functions.miscTab1_support_functions as miscTab1
import support_functions.miscTab2_support_functions as miscTab2
import support_functions.general_functions as general
import support_functions.empty as empty

#import for splash screen with pyinstaller whenever exe is run
if getattr(sys, 'frozen', False):
    import pyi_splash

#root config
root = Tk()
root.title("NJIT Flylanders™ AeroCalc")
canvas = Canvas()
windowWidth = 640
windowHeight=630
root.geometry(f'{windowWidth}x{windowHeight}')
root.resizable(False, False)

try:
    imgPath = general.addImg("aeroLogo.png")
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

#Change color/font styles here
colorSelection= "lightgray"
bgThickness=15
fontName = "Roboto"

def destroyTabs() -> None:
    '''Destroys the currently open tabs'''
    for item in tabControl.winfo_children():
        item.destroy()

def wingActivate() -> None:
    '''Display tabs for tail subteam calculators'''
    tab1 = setupWindow("Wing")
    tabControl.add(tab1, text="Aspect/Taper Ratio", state=NORMAL)
    tabControl.grid(column=1, row=0, sticky='nsew')

    wingTab1.constructTab(tab1, colorSelection, fontName)

def tailActivate() -> None:
    '''Display tabs for tail subteam calculators'''
    tab1 = setupWindow("Tail")

    tabControl.add(tab1, text ='Volume Ratio', state=NORMAL)
    tabControl.grid(column=1, row=0, sticky='nsew')

    tailTab1.constructTab(tab1, colorSelection, fontName, bgThickness)

def homeActivate() -> None:
    '''Display home page'''
    tab1 = setupWindow("Home")
    homepage.constructTab(tabControl, tab1, colorSelection)

def electronicsActivate() -> None:
    '''Display electronics calculators'''
    tab1 = setupWindow("Electronics")

    #Tab 1
    tabControl.add(tab1, text ='Thrust Plot Automation', state=NORMAL)
    tabControl.grid(column=2, row=0, sticky='nsew')

    elecTab1.constructTab(tab1, colorSelection, fontName)

def landgearActivate() -> None:
    '''Display landing gear calculators'''
    tab1 = setupWindow("Landing Gear")
    empty.initEmpty(tabControl, tab1, fontName, colorSelection)

def fuselageActivate() -> None:
    '''Display fuselage calculators'''
    tab1 = setupWindow("Fuselage")
    empty.initEmpty(tabControl, tab1, fontName, colorSelection)

def miscActivate() -> None:
    '''Display miscellaneous calculators'''
    tab1 = setupWindow("Misc")
    tab2 = Frame(tabControl, width=windowWidth, height=windowHeight)
    tabControl.add(tab1, text="Competition Scoring", state=NORMAL)
    #tabControl.add(tab2, text="Takeoff Distance", state=NORMAL)
    tabControl.grid(column=1, row=0, sticky='nsew')

    miscTab1.constructTab(tab1, colorSelection, fontName)
    #miscTab2.constructTab(tab2, colorSelection, fontName)

#Buttons setup
buttons = Frame(root, width=100, height=1000, bg="lightgray")
buttons.grid(row=0, column=0, sticky='n')
buttonColor = "#b40707"
buttonText = "Roboto 12 bold"
reliefStyle="solid"
buttonTextColor = "black"
buttonHeight = 4

buttonList = {}
rowNum = 0
def createButton(btnName: str, funName, btnText: str):
    global rowNum
    currBtn = Button(buttons, text=btnText, command=funName, font=buttonText, height=buttonHeight, bg=buttonColor, relief=reliefStyle, fg=buttonTextColor)
    currBtn.grid(row=rowNum, column=0, sticky='new')
    buttonList[btnName] = currBtn
    rowNum+=1

#         button name, function, text to display)
createButton("Home", homeActivate, "Home")
createButton("Wing", wingActivate, "Wing")
createButton("Tail", tailActivate, "Tail")
createButton("Electronics", electronicsActivate, "Electronics")
createButton("Landing Gear", landgearActivate, "Landing\nGear")
createButton("Fuselage", fuselageActivate, "Fuselage")
createButton("Misc", miscActivate, "Misc.")

def resetButtonColors() -> None:
    '''Set the buttons for changing the tabs back to their original color before they were the active window'''
    for button in buttonList.values():
        button.config(fg=buttonTextColor, bg=buttonColor)

def activateButtonColor(currButton: Button) -> None:
    '''Sets the button to the active window colors'''
    activeButton = buttonList[currButton]
    activeButton.config(fg="white", bg="black")

def setupWindow(currBtn: str) -> Frame:
    '''Call the proper functions to clear out the last tab and setup the current window.
        Returns the new Frame.
    '''
    destroyTabs()
    resetButtonColors()
    activateButtonColor(currBtn)
    newTab = Frame(tabControl, width=windowWidth, height=windowHeight, bg=colorSelection)
    return newTab

if __name__ == "__main__":
    homeActivate() #start with home page displaying to user
    if getattr(sys, 'frozen', False):
        pyi_splash.close()
    root.mainloop()
    
    #kill the processes when application is closed
    root.protocol("WM_DELETE_WINDOW", sys.exit(0))