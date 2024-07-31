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
import support_functions.tailTab1_support_functions as tailTab1
import support_functions.tailTab2_support_functions as tailTab2
import support_functions.elecTab1_support_functions as elecTab1
import support_functions.empty as empty

#root config
root = Tk()
root.title("NJIT Flylanders™ AeroCalc")
canvas = Canvas()
windowWidth = 620
windowHeight=540
root.geometry(f'{windowWidth}x{windowHeight}'.format())
root.resizable(False, False)

try:
    photo = PhotoImage(file = "./images/aeroLogo.png")
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

def tailActivate() -> None:
    '''Show tabs for wing and tail subteam calculators'''
    tab1 = setupWindow("Tail")
    tab2 = Frame(tabControl, width=565, height=550, bg=colorSelection)

    tabControl.add(tab1, text ='Volume Ratio', state=NORMAL)
    tabControl.add(tab2, text ='Aspect/Taper Ratio', state=NORMAL)
    tabControl.grid(column=1, row=0, sticky='nsew')

    tailTab1.constructTab(tab1, colorSelection, fontName, bgThickness)
    tailTab2.constructTab(tab2, colorSelection, fontName)

def homeActivate() -> None:
    '''Display home page'''
    global aeroLogo #declared PhotoImage as global to avoid garbage collection
    tab1 = setupWindow("Home")

    #Tab 1
    tabControl.add(tab1, text="Home", state=NORMAL)
    tabControl.grid(column=1, row=0, sticky='nsew')
    homeTitle = Label(tab1, text="Flylanders™ AeroCalc", bg=colorSelection, font="Roboto 20 bold")
    homeTitle.grid(row=0, column=0, columnspan=10, sticky='nsew', padx=120)

    welcomeText = Label(tab1, wraplength=400, font="Roboto 14", bg=colorSelection, text="Welcome to AeroCalc, created by and for the NJIT Flylanders™ SAE Aero Design Team.")
    welcomeText.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=75, pady=(10, 0))

    aeroLogo = PhotoImage(file="./images/aeroLogo.png")
    aeroPhoto = Label(tab1, image = aeroLogo, width=200, height=200, bg=colorSelection)
    aeroPhoto.grid(row=2, column=0, columnspan=2, sticky='nsew', padx = 150, pady=20)

    descrText = Label(tab1, wraplength=400, font="Roboto 14", bg=colorSelection, text="This program is a compilation of calculators and tools used by each of our subteams to design our competition RC plane.")
    descrText.grid(row=3, column=0, columnspan=2, sticky='nsew')

    creditText = Label(tab1, wraplength=200, font="Roboto 10", bg=colorSelection, text="Created By: Lindsay Burke")
    creditText.grid(row=4, column=0, sticky='sw', pady=(60, 0), padx=(10, 0))

    versionText = Label(tab1, font="Roboto 10", bg=colorSelection, text="v1.0.0")
    versionText.grid(row=4, column=1, sticky='se', padx=(0, 30), pady=(60, 0))

def electronicsActivate() -> None:
    '''Display electronics calculators'''
    tab1 = setupWindow("Electronics")

    #Tab 1
    tabControl.add(tab1, text ='Thrust Automation', state=NORMAL)
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
    tab1 = setupWindow("Misc")
    empty.initEmpty(tabControl, tab1, fontName, colorSelection)

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

createButton("Home", homeActivate, "Home")
createButton("Tail", tailActivate, "Wing/Tail")
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
    root.mainloop()