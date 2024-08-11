import support_functions.tailTab1_support_functions as tailTab1
import support_functions.elecTab1_support_functions as elecTab1
import support_functions.homepage_support_functions as homepage
import support_functions.wingTab1_support_functions as wingTab1
import support_functions.miscTab1_support_functions as miscTab1
import support_functions.miscTab2_support_functions as miscTab2
import support_functions.empty as empty
from tkinter import *

class GeneralWindowFunctions:
    def __init__(self, tabControl, windowDimensions: tuple[int], colorSelection: str,
                 fontName: str, buttonList: list[Button], buttonTextColor: str,
                 buttonColor: str, buttonHeight: int, buttonText: str):
        self.tabControl = tabControl
        self.windowWidth = windowDimensions[0]
        self.windowHeight = windowDimensions[1]
        self.colorSelection = colorSelection
        self.fontName = fontName
        self.buttonList = buttonList
        self.buttonTextColor = buttonTextColor
        self.buttonColor = buttonColor
        self.buttonHeight = buttonHeight
        self.buttonText = buttonText

    def destroyTabs(self) -> None:
        '''Destroys the currently open tabs'''
        for item in self.tabControl.winfo_children():
            item.destroy()

    def resetButtonColors(self) -> None:
        '''Set the buttons for changing the tabs back to their original color before they were the active window'''
        for button in self.buttonList.values():
            button.config(fg=self.buttonTextColor, bg=self.buttonColor)

    def activateButtonColor(self, currButton: Button) -> None:
        '''Sets the button to the active window colors'''
        activeButton = self.buttonList[currButton]
        activeButton.config(fg="white", bg="black")

    def createButton(self, btnName: str, funName, btnText: str, buttons: Frame):
        currBtn = Button(buttons, text=btnText, command=funName, font=self.buttonText, height=self.buttonHeight, bg=self.buttonColor, fg=self.buttonTextColor)
        currBtn.grid(row=len(self.buttonList), column=0, sticky='new')
        self.buttonList[btnName] = currBtn

    def setupWindow(self, currBtn: str) -> Frame:
        '''Call the proper functions to clear out the last tab and setup the current window.
            Returns the new Frame.
        '''
        self.destroyTabs()
        self.resetButtonColors()
        self.activateButtonColor(currBtn)
        newTab = Frame(self.tabControl, width=self.windowWidth, height=self.windowHeight, bg=self.colorSelection)
        return newTab

    def wingActivate(self) -> None:
        '''Display tabs for tail subteam calculators'''
        tab1 = self.setupWindow("Wing")
        self.tabControl.add(tab1, text="Aspect/Taper Ratio", state=NORMAL)
        self.tabControl.grid(column=1, row=0, sticky='nsew')

        wingTab1.constructTab(tab1, self.colorSelection, self.fontName)

    def tailActivate(self) -> None:
        '''Display tabs for tail subteam calculators'''
        tab1 = self.setupWindow("Tail")

        self.tabControl.add(tab1, text ='Volume Ratio', state=NORMAL)
        self.tabControl.grid(column=1, row=0, sticky='nsew')

        tailTab1.constructTab(tab1, self.colorSelection, self.fontName)

    def homeActivate(self) -> None:
        '''Display home page'''
        tab1 = self.setupWindow("Home")
        homepage.constructTab(self.tabControl, tab1, self.colorSelection)

    def electronicsActivate(self) -> None:
        '''Display electronics calculators'''
        tab1 = self.setupWindow("Electronics")

        #Tab 1
        self.tabControl.add(tab1, text ='Thrust Plot Automation', state=NORMAL)
        self.tabControl.grid(column=2, row=0, sticky='nsew')

        elecTab1.constructTab(tab1, self.colorSelection, self.fontName)

    def landgearActivate(self) -> None:
        '''Display landing gear calculators'''
        tab1 = self.setupWindow("Landing Gear")
        empty.initEmpty(self.tabControl, tab1, self.fontName, self.colorSelection)

    def fuselageActivate(self) -> None:
        '''Display fuselage calculators'''
        tab1 = self.setupWindow("Fuselage")
        empty.initEmpty(self.tabControl, tab1, self.fontName, self.colorSelection)

    def miscActivate(self) -> None:
        '''Display miscellaneous calculators'''
        tab1 = self.setupWindow("Misc")
        tab2 = Frame(self.tabControl, width=self.windowWidth, height=self.windowHeight)
        self.tabControl.add(tab1, text="Competition Scoring", state=NORMAL)
        #tabControl.add(tab2, text="Takeoff Distance", state=NORMAL)
        self.tabControl.grid(column=1, row=0, sticky='nsew')

        miscTab1.constructTab(tab1, self.colorSelection, self.fontName)
        #miscTab2.constructTab(tab2, colorSelection, fontName)