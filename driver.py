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
import tailTab1_support_functions, tailTab2_support_functions, elecTab1_support_functions, empty

#root config
root = Tk()
root.title("NJIT Flylanders™ AeroCalc")
canvas = Canvas()
root.geometry('620x545')
root.resizable(False, False)

#Change color/font styles here
colorSelection = "lightgray"
bgThickness = 15
fontName = "Roboto"

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

def destroyTabs() -> None:
    '''Destroys the currently open tabs'''
    for item in tabControl.winfo_children():
        item.destroy()

def wingActivate() -> None:
    '''Show tabs for wing and tail subteam calculators'''
    tab1 = setupWindow(wingBtn)

    tab2 = Frame(tabControl, width=565, height=550, bg=colorSelection)

    tabControl.add(tab1, text ='Volume Ratio', state=NORMAL)
    tabControl.add(tab2, text ='Aspect/Taper Ratio', state=NORMAL)
    tabControl.grid(column=1, row=0, sticky='nsew')

    tailTab1_support_functions.constructTab(tab1, colorSelection, fontName, bgThickness)
    tailTab2_support_functions.constructTab(tab2, colorSelection, fontName)

def homeActivate() -> None:
    '''Display home page'''
    global aeroLogo #declared PhotoImage as global to avoid garbage collection
    tab1 = setupWindow(homeBtn)

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
    tab1 = setupWindow(electronicsBtn)

    '''
    Tab 1 -- Thrust Stand Data Visualization
    '''
    tabControl.add(tab1, text ='Thrust Automation', state=NORMAL)
    tabControl.grid(column=2, row=0, sticky='nsew')

    elecTab1_support_functions.constructTab(tab1, colorSelection, fontName)

def landgearActivate() -> None:
    '''Display landing gear calculators'''
    tab1 = setupWindow(landgearBtn)
    empty.initEmpty(tabControl, tab1, fontName, colorSelection)

def fuselageActivate() -> None:
    '''Display fuselage calculators'''
    tab1 = setupWindow(fuselageBtn)
    empty.initEmpty(tabControl, tab1, fontName, colorSelection)

def miscActivate() -> None:
    tab1 = setupWindow(miscBtn)
    empty.initEmpty(tabControl, tab1, fontName, colorSelection)

#Add buttons to navigate between the different subteams
buttons = Frame(root, width=200, height=1000, bg="lightgray")
buttons.grid(row=0, column=0, sticky='n')
buttonColor = "#b40707"
buttonText = "Roboto 12 bold"
reliefStyle="solid"
buttonTextColor = "black"
buttonHeight = 4

homeBtn = Button(buttons, text="Home", command=homeActivate, font=buttonText, height=buttonHeight, bg=buttonColor, relief=reliefStyle, fg=buttonTextColor)
homeBtn.grid(row=0, column=0, sticky='new')
wingBtn = Button(buttons, text="Wing/Tail", command=wingActivate, font=buttonText, height=buttonHeight, bg=buttonColor, relief=reliefStyle, fg=buttonTextColor)
wingBtn.grid(row=1, column=0, sticky='new')
electronicsBtn = Button(buttons, text="Electronics", command=electronicsActivate, font=buttonText, height=buttonHeight, bg=buttonColor, relief=reliefStyle, fg=buttonTextColor)
electronicsBtn.grid(row=2, column=0, sticky='new')
landgearBtn = Button(buttons, text="Landing\nGear", command=landgearActivate, font=buttonText, height=buttonHeight, bg=buttonColor, relief=reliefStyle, fg=buttonTextColor)
landgearBtn.grid(row=3, column=0, sticky='new')
fuselageBtn = Button(buttons, text="Fuselage", command=fuselageActivate, font=buttonText, height=buttonHeight, bg=buttonColor, relief=reliefStyle, fg=buttonTextColor)
fuselageBtn.grid(row=4, column=0, sticky='new')
miscBtn = Button(buttons, text="Misc.", command=miscActivate, font=buttonText, height=buttonHeight, bg=buttonColor, relief=reliefStyle, fg=buttonTextColor)
miscBtn.grid(row=5, column=0, sticky='new')

buttonList = [homeBtn, wingBtn, electronicsBtn, landgearBtn, miscBtn, fuselageBtn]
def resetButtonColors() -> None:
    '''Set the buttons for changing the tabs back to their original color before they were the active window'''
    for button in buttonList:
        button.config(fg=buttonTextColor, bg=buttonColor)

def activateButtonColor(activeButton: Button) -> None:
    '''Sets the button to the active window colors'''
    activeButton.config(fg="white", bg="black")

def setupWindow(currBtn: Button) -> Frame:
    '''Call the proper functions to clear out the last tab and setup the current one.
        This returns the first tab as a Frame.
    '''
    destroyTabs()
    resetButtonColors()
    activateButtonColor(currBtn)

    tab1 = Frame(tabControl, width=620, height=545, bg=colorSelection)
    return tab1

root.config(bg=colorSelection)

homeActivate() #start with home page displaying to user
root.mainloop()