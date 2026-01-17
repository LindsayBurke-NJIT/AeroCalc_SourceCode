import support_functions.tailTab1_support_functions as tailTab1
import support_functions.elecTab1_support_functions as elecTab1
import support_functions.elecTab2_support_functions as elecTab2
import support_functions.elecTab3_support_functions as elecTab3
import support_functions.homepage_support_functions as homepage
import support_functions.wingTab1_support_functions as wingTab1
import support_functions.miscTab1_support_functions as miscTab1
import support_functions.miscTab2_support_functions as miscTab2
import support_functions.empty as empty
from tkinter import *

class ScrollableFrame(Frame):
    '''A frame that can scroll its content if it exceeds the available space'''
    def __init__(self, parent, bg="lightgray", **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        
        # Create canvas and scrollbar
        self.canvas = Canvas(self, bg=bg, highlightthickness=0)
        scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg=bg)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack the canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel scrolling
        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<Button-4>", self._on_mousewheel)
        self.scrollable_frame.bind("<Button-5>", self._on_mousewheel)
    
    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
    
    def get_scrollable_frame(self):
        '''Returns the frame where widgets should be placed'''
        return self.scrollable_frame

class GeneralWindowFunctions:
    def __init__(self, tabControl, windowDimensions: tuple[int], colorSelection: str,
                 fontName: str, buttonList: list[Button], buttonTextColor: str,
                 buttonColor: str, buttonHeight: int, buttonText: str, buttonRelief: str):
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
        self.buttonRelief = buttonRelief

        self.openTabs = []

    def destroyTabs(self) -> None:
        '''Destroys the currently open tabs'''
        for item in self.tabControl.winfo_children():
            item.destroy()
        self.openTabs.clear()

    def resetButtonColors(self) -> None:
        '''Set the buttons for changing the tabs back to their original color before they were the active window'''
        for button in self.buttonList.values():
            button.config(fg=self.buttonTextColor, bg=self.buttonColor)

    def activateButtonColor(self, currButton: Button) -> None:
        '''Sets the button to the active window colors'''
        activeButton = self.buttonList[currButton]
        activeButton.config(fg="white", bg="black")

    def createButton(self, btnName: str, funName, btnText: str, buttons: Frame):
        currBtn = Button(buttons, text=btnText, command=funName, font=self.buttonText, height=self.buttonHeight, relief=self.buttonRelief, bg=self.buttonColor, fg=self.buttonTextColor)
        currBtn.grid(row=len(self.buttonList), column=0, sticky='new')
        buttons.rowconfigure(len(self.buttonList), weight=1)
        buttons.columnconfigure(len(self.buttonList), weight=1)

        self.buttonList[btnName] = currBtn

    def setupWindow(self, currBtn: str) -> None:
        '''Call the proper functions to clear out the last tab and setup the current window.
        '''
        self.destroyTabs()
        self.resetButtonColors()
        self.activateButtonColor(currBtn)

    def addTab(self, tabClass, tabName: str) -> Frame:
        newTab = ScrollableFrame(self.tabControl, bg=self.colorSelection)
        self.openTabs.append(newTab)
        self.tabControl.add(newTab, text=tabName, state=NORMAL)
        # Configure grid weights for responsive layout
        newTab.rowconfigure(0, weight=1)
        newTab.columnconfigure(0, weight=1)
        # Return the scrollable frame for content placement
        return newTab.get_scrollable_frame()

    def wingActivate(self) -> None:
        '''Display tabs for tail subteam calculators'''
        self.setupWindow("Wing")
        tab1 = self.addTab(wingTab1,"Aspect/Taper Ratio")

        wingTab1.constructTab(tab1, self.colorSelection, self.fontName)

    def tailActivate(self) -> None:
        '''Display tabs for tail subteam calculators'''
        self.setupWindow("Tail")

        tab1 = self.addTab(tailTab1, "Volume Ratio")

        myTab = tailTab1.TailTab1(tab1, self.colorSelection, self.fontName)
        myTab.constructTab()

    def homeActivate(self) -> None:
        '''Display home page'''
        self.setupWindow("Home")
        
        tab1 = self.addTab(homepage, "Home")
        homepage.constructTab(self.tabControl, tab1, self.colorSelection)

    def electronicsActivate(self) -> None:
        '''Display electronics calculators'''
        self.setupWindow("Electronics")

        tab1 = self.addTab(elecTab1, "Thrust Plot Automation")
        elecTab1.constructTab(tab1, self.colorSelection, self.fontName)

        tab2 = self.addTab(elecTab2, "Servo Torque Calculator")
        elecTab2.constructTab(tab2, self.colorSelection, self.fontName)

        tab3 = self.addTab(elecTab3, "Voltage Drop Calculator")
        elecTab3.constructTab(tab3, self.colorSelection, self.fontName)

    def landgearActivate(self) -> None:
        '''Display landing gear calculators'''
        self.setupWindow("Landing Gear")

        tab1 = self.addTab(empty, "Empty")
        empty.initEmpty(self.tabControl, tab1, self.fontName, self.colorSelection)

    def fuselageActivate(self) -> None:
        '''Display fuselage calculators'''
        self.setupWindow("Fuselage")

        tab1 = self.addTab(empty, "Empty")
        empty.initEmpty(self.tabControl, tab1, self.fontName, self.colorSelection)

    def miscActivate(self) -> None:
        '''Display miscellaneous calculators'''
        self.setupWindow("Misc")

        tab1 = self.addTab(miscTab1, "Competition Scoring")
        miscTab1.constructTab(tab1, self.colorSelection, self.fontName)

        tab2 = self.addTab(miscTab2, "Takeoff Distance")
        miscTab2.constructTab(tab2, self.colorSelection, self.fontName)