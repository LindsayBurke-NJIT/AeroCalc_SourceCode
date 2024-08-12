"""Tab1 -- Volume Ratio"""
from tkinter import *
class TailTab1:
    def __init__(self, tab1, colorSelection, fontName):
        self.wingArea = 0
        self.chord = 0
        self.tailArea = 0
        self.myLength = 0
        self.vTailArea = 0
        self.vLength = 0
        self.wingSpan = 0
        self.chordLabel = Label(tab1, text="Mean Aerodynamic Chord", bg=colorSelection,  highlightcolor=colorSelection, highlightbackground=colorSelection, font=fontName+" 12 bold")
        self.chordInput = Entry(tab1)
        self.tailLabel = Label(tab1, text="Horizontal Tail Area", bg=colorSelection, highlightcolor=colorSelection, highlightbackground=colorSelection, font=fontName+" 12 bold")
        self.tailInput = Entry(tab1)
        self.lengthLabel = Label(tab1, text="Length between aerodynamic centers \nof the wing and horizontal tailplane", bg=colorSelection, highlightcolor=colorSelection, highlightbackground=colorSelection, font=fontName+" 12 bold")
        self.lengthInput = Entry(tab1)
        self.vTailLabel = Label(tab1, text="Vertical Tail Area", bg=colorSelection, highlightcolor=colorSelection, highlightbackground=colorSelection, font=fontName+" 12 bold")
        self.vTailInput = Entry(tab1)
        self.wingLabel = Label(tab1, text="Wing Area", bg=colorSelection,highlightcolor=colorSelection, highlightbackground=colorSelection, font=fontName+" 12 bold")
        self.wingInput = Entry(tab1)
        self.wingSpanLabel = Label(tab1, text="Wing Span", bg=colorSelection, highlightcolor=colorSelection, highlightbackground=colorSelection, font=fontName+" 12 bold")
        self.wingSpanInput = Entry(tab1)
        self.vLengthLabel = Label(tab1, text="Length between aerodynamic centers \nof the wing and vertical tailplane", bg=colorSelection, highlightcolor=colorSelection, highlightbackground=colorSelection, font=fontName+" 12 bold")
        self.vLengthInput = Entry(tab1)
        self.outputLabel = Label(tab1, text="Volume Ratio:", bg=colorSelection, font=fontName+" 13 bold")
        self.outputBox = Text(tab1, width=20, height=5, font=fontName+" 13")
        self.tab = tab1
        self.clicked = StringVar()
        self.colorSelection = colorSelection
        self.fontName = fontName

    def submitDrop(self, value) -> None:
        '''This function adds the proper labels and input boxes 
        based on whether horizontal or vertical stabilizer was selected
        '''
        horizontalWidgets = [self.chordLabel, self.chordInput, self.tailLabel, self.tailInput, self.lengthLabel, self.lengthInput]
        verticalWidgets = [self.vTailLabel, self.vTailInput, self.wingSpanLabel, self.wingSpanInput, self.vLengthLabel, self.vLengthInput]

        if(value=="Horizontal"):
            for widget in verticalWidgets:
                widget.grid_remove()

            #Chord field entry
            self.chordLabel.grid(row=4,column=1) 
            self.chordInput.grid(row=4, column=2)
                    
            #Horizontal tail area field entry
            self.tailLabel.grid(row=5,column=1)
            self.tailInput.grid(row=5, column=2)

            #Length field entry
            self.lengthLabel.grid(row=6,column=1) 
            self.lengthInput.grid(row=6, column=2)
        else:
            for widget in horizontalWidgets:
                widget.grid_remove()

            #Vertical wing area field entry
            self.vTailLabel.grid(row=4,column=1, padx=10, pady=(0,30))
            self.vTailInput.grid(row=4, column=2, pady=(0,30))

            #Wing span field entry
            self.wingSpanLabel.grid(row=5, column=1, padx=10, pady=(0,30))
            self.wingSpanInput.grid(row=5, column=2, pady=(0,30))

            #Length field entry
            self.vLengthLabel.grid(row=6,column=1, padx=10, pady=(0,30)) 
            self.vLengthInput.grid(row=6, column=2, pady=(0,30))

    def constructTab(self) -> None:
        '''Creates all of the Tkinter widgets'''
        #Creates dropdown menu
        options = ["Horizontal", "Vertical"]
        self.clicked.set("Horizontal")
        titleText = Label(self.tab, text="Volume Ratio Calculator", bg=self.colorSelection, font=self.fontName+' 15 bold')
        titleText.grid(row=0, column=1, pady=10, columnspan=2)
        dropText = Label(self.tab, text="Select Stabilizer Type:", bg=self.colorSelection,font=self.fontName+' 13 bold')
        dropText.grid(row=1, column=1, pady=10, columnspan=2)
        dropDown = OptionMenu(self.tab, self.clicked, *options, command=self.submitDrop)
        dropDown.grid(row=2, columnspan=3, padx=(0, 20), pady=(0, 30))

        #Chord field entry
        self.chordLabel.grid(row=4,column=1, padx=10, pady=(0,30)) 
        self.chordInput.grid(row=4, column=2, pady=(0,30))
                
        #Horizontal tail area field entry
        self.tailLabel.grid(row=5,column=1, padx=10, pady=(0,30)) 
        self.tailInput.grid(row=5, column=2, pady=(0,30))

        #Length field entry
        self.lengthLabel.grid(row=6,column=1, padx=10, pady=(0,30)) 
        self.lengthInput.grid(row=6, column=2, pady=(0,30))

        #Wing area field entry
        self.wingLabel.grid(row=3,column=1, padx=10, pady=(0,30))
        self.wingInput.grid(row=3, column=2, pady=(0,30))

        #Output box setup
        self.outputLabel.grid(row=8, column=2, pady=(10,0), padx=(0, 0))
        self.outputBox.grid(row=9, column=2, padx=(25,20), sticky='w')
        self.outputBox.configure(state=DISABLED)

        #Defines all buttons
        startButton = Button(self.tab, text="Calculate", command=self.submitAll, width=7, height=2, bg="greenyellow",                                                              font=self.fontName, relief="sunken")
        startButton.grid(sticky='nw', row=9, column=1, padx=(23,0))

        resetButton = Button(self.tab, text="Clear \nInput", command=self.resetAll, width=7, height=2, bg="cornflowerblue",                                                           font=self.fontName, relief="sunken")
        resetButton.grid(sticky="ne", row=9, column=1, padx=(0, 20))

        clearOutputButton = Button(self.tab, text="Clear \nOutput", command=self.clearOutput, width=7, height=2, bg="cornflowerblue", font=self.fontName, relief="sunken")
        clearOutputButton.grid(sticky='n', row=9, column=1)

    def resetAll(self) -> None:
        '''This function clears all input boxes'''
        if(self.clicked.get()=="Horizontal"):
            self.tailInput.delete(0,"end")
            self.lengthInput.delete(0,"end")
            self.wingSpanInput.delete(0,"end")
            self.chordInput.delete(0,"end")
        elif(self.clicked.get()=="Vertical"):
            self.vTailInput.delete(0,"end")
            self.wingSpanInput.delete(0,"end")
            self.vLengthInput.delete(0,"end")
        self.wingInput.delete(0, "end")

    def clearOutput(self) -> None:
        self.outputBox.configure(state=NORMAL)
        self.outputBox.delete("1.0", "end")
        self.outputBox.configure(state=DISABLED)

    def setValues(self) -> bool:
        '''This function takes user entered values from the input boxes
        and assigns to vars for ease of calculations. Returns boolean that
        is True when the values are correctly set, and False otherwise.
        '''
        try:
            if(self.clicked.get()=="Horizontal"):
                self.wingArea = float(self.wingInput.get())
                self.chord = float(self.chordInput.get())
                self.tailArea = float(self.tailInput.get())
                self.myLength = float(self.lengthInput.get())

                if(self.wingArea<0 or self.chord<0 or self.tailArea<0 or self.myLength<0):
                    self.addError("Values cannot be negative")
                    return False
            if(self.clicked.get()=="Vertical"):
                self.vTailArea = float(self.vTailInput.get())
                self.vLength = float(self.vLengthInput.get())
                self.wingSpan = float(self.wingSpanInput.get())
                self.wingArea = float(self.wingInput.get())

                if(self.vTailArea<0 or self.vLength<0 or self.wingSpan<0 or self.wingArea<0):
                    self.addError("Values cannot be negative")
                    return False
            return True
        except:
            return False

    def addError(self, e: str):
        self.outputBox.configure(state=NORMAL)
        self.outputBox.tag_configure("redText", foreground="red")
        self.outputBox.insert("1.0", f"Error: {e}\n", "redText")
        self.outputBox.configure(state=DISABLED)

    def addAnswer(self, ans: float):
        self.outputBox.configure(state=NORMAL, fg="black")
        ans = "%.5f" % ans #format answer to five decimal places
        self.outputBox.insert("1.0", str(ans)+"\n")
        self.outputBox.configure(state=DISABLED)

    def submitAll(self) -> int:
        '''Calculates volume ratio, outputs calculation to widget, and 
        returns the volume ratio as an integer'''
        isSet = self.setValues()
        if(isSet):
            try:
                if(self.clicked.get()=="Horizontal"):
                    self.outputBox.configure(state=NORMAL)
                    h_volumeRatio = (self.tailArea*self.myLength)/(self.wingArea*self.chord) #Calculates the volume ratio for horizontal stabilizer
                    self.addAnswer(h_volumeRatio)
                    return h_volumeRatio
                elif(self.clicked.get()=="Vertical"):
                    self.outputBox.configure(state=NORMAL)
                    v_volumeRatio = (self.vTailArea*self.vLength)/(self.wingArea*self.wingSpan) #Calculates the volume ratio for vertical stabilizer
                    self.addAnswer(v_volumeRatio)
                    return v_volumeRatio
            except ZeroDivisionError:
                self.addError("Division by Zero")
        else:
            self.addError("Incorrect Input")