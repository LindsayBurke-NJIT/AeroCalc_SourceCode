"""Tab1 -- Volume Ratio"""
from tkinter import *
import support_functions.TailTab1 as tt1

obj = tt1.TailTab1()
def constructTab(tab1: Frame, colorSelection: str, fontName: str, bgThickness: int) -> None:
    '''Creates all of the Tkinter widgets'''
    #Creates dropdown menu
    options = ["Horizontal", "Vertical"]
    clicked = StringVar()
    clicked.set("Horizontal")
    dropText = Label(tab1, text="Select Stabilizer Type:", bg=colorSelection,font=fontName+' 15 bold')
    dropText.grid(row=1, column=1, pady=10, columnspan=3)
    dropDown = OptionMenu(tab1, clicked, *options)
    dropDown.grid(row=2, columnspan=3)

    #Chord field entry
    chordLabel = Label(tab1, text="Mean Aerodynamic Chord", bg=colorSelection,  highlightcolor=colorSelection, highlightbackground=colorSelection, highlightthickness=bgThickness, font=fontName+" 12 bold")
    chordLabel.grid(row=4,column=1, padx=10) 
    chordInput = Entry(tab1)
    chordInput.grid(row=4, column=2)
            
    #Horizontal tail area field entry
    tailLabel = Label(tab1, text="Horizontal Tail Area", bg=colorSelection, highlightcolor=colorSelection, highlightbackground=colorSelection, highlightthickness=bgThickness, font=fontName+" 12 bold")
    tailLabel.grid(row=5,column=1, padx=10) 
    tailInput = Entry(tab1)
    tailInput.grid(row=5, column=2)

    #Length field entry
    lengthLabel = Label(tab1, text="Length between aerodynamic centers \nof the wing and horizontal tailplane", bg=colorSelection, highlightcolor=colorSelection, highlightbackground=colorSelection, highlightthickness=bgThickness, font=fontName+" 12 bold")
    lengthLabel.grid(row=6,column=1, padx=10) 
    lengthInput = Entry(tab1)
    lengthInput.grid(row=6, column=2)

    #Wing area field entry
    wingLabel = Label(tab1, text="Wing Area", bg=colorSelection,highlightcolor=colorSelection, highlightbackground=colorSelection, highlightthickness=bgThickness, font=fontName+" 12 bold")
    wingLabel.grid(row=3,column=1, padx=10)
    wingInput = Entry(tab1)
    wingInput.grid(row=3, column=2)

    #Vertical stabilizer setup
    vTailLabel = Label(tab1, text="Vertical Tail Area", bg=colorSelection, highlightcolor=colorSelection, highlightbackground=colorSelection, highlightthickness=bgThickness, font=fontName+" 12 bold")
    vTailInput = Entry(tab1)
    wingSpanLabel = Label(tab1, text="Wing Span", bg=colorSelection, highlightcolor=colorSelection, highlightbackground=colorSelection, highlightthickness=bgThickness, font=fontName+" 12 bold")
    wingSpanInput = Entry(tab1)
    vLengthLabel = Label(tab1, text="Length between aerodynamic centers \nof the wing and vertical tailplane", bg=colorSelection, highlightcolor=colorSelection, highlightbackground=colorSelection, highlightthickness=bgThickness, font=fontName+" 12 bold")
    vLengthInput = Entry(tab1)

    #Output box setup
    outputLabel = Label(tab1, text="Volume Ratio:", bg="grey", font=fontName+" 13 bold")
    outputLabel.grid(row=8, column=2, pady=(10,0), padx=(0, 30))
    outputBox = Text(tab1, width=20, height=5, font=fontName+" 13")
    outputBox.grid(row=9, column=2, padx=(0,20), sticky='w')
    outputBox.configure(state=DISABLED)

    #Defines all buttons
    dropButton = Button(tab1, text="Select", command=lambda: submitDrop(tab1, clicked, colorSelection, fontName, bgThickness, outputBox,
                                                                        chordLabel, chordInput, tailLabel, tailInput, lengthLabel, lengthInput,
                                                                        vTailLabel, vTailInput, wingSpanLabel, wingSpanInput, vLengthLabel, vLengthInput), 
                        width=6, height=1, bg="cornflowerblue", font=fontName+" 8")
    dropButton.grid(row=2, column=2, columnspan=2, padx=(0, 190))

    startButton = Button(tab1, text="Calculate", command=lambda: submitAll(clicked, outputBox, wingInput, 
                                                                           chordInput, tailInput, lengthInput, 
                                                                           vTailInput, vLengthInput, wingSpanInput),
                                                                           width=7, height=2, bg="greenyellow", 
                                                                           font=fontName, relief="sunken")
    startButton.grid(sticky='nw', row=9, column=1, padx=(23,0))

    resetButton = Button(tab1, text="Clear \nInput", command=lambda: resetAll(clicked, tailInput, lengthInput, wingSpanInput, chordInput, vTailInput, vLengthInput, wingInput), width=7, height=2, bg="cornflowerblue", font=fontName, relief="sunken")
    resetButton.grid(sticky="ne", row=9, column=1, padx=(0, 20))

    clearOutputButton = Button(tab1, text="Clear \nOutput", command=lambda: clearOutput(outputBox), width=7, height=2, bg="cornflowerblue", font=fontName, relief="sunken")
    clearOutputButton.grid(sticky='n', row=9, column=1)

def submitDrop(tab1: Frame, clicked: StringVar, colorSelection: str, fontName: str, bgThickness: int, outputBox: Text,
               chordLabel: Label, chordInput: Text,
               tailLabel: Label, tailInput: Text,
               lengthLabel: Label, lengthInput: Text,
               vTailLabel: Label, vTailInput: Text,
               wingSpanLabel: Label, wingSpanInput: Text,
               vLengthLabel: Label, vLengthInput: Text) -> None:
    '''This function adds the proper labels and input boxes 
    based on whether horizontal or vertical stabilizer was selected
    '''
    horizontalWidgets = [chordLabel, chordInput, tailLabel, tailInput, lengthLabel, lengthInput]
    verticalWidgets = [vTailLabel, vTailInput, wingSpanLabel, wingSpanInput, vLengthLabel, vLengthInput]

    rowIndex = 4 #start at row 4 for user input boxes
    if(clicked.get()=="Horizontal"):
        for widget in verticalWidgets:
            widget.grid_remove()

        #Chord field entry
        chordLabel.grid(row=4,column=1) 
        chordInput.grid(row=4, column=2)
                
        #Horizontal tail area field entry
        tailLabel.grid(row=5,column=1)
        tailInput.grid(row=5, column=2)

        #Length field entry
        lengthLabel.grid(row=6,column=1, padx=10) 
        lengthInput.grid(row=6, column=2)
    else:
        for widget in horizontalWidgets:
            widget.grid_remove()

        #Vertical wing area field entry
        vTailLabel.grid(row=4,column=1, padx=10)
        vTailInput.grid(row=4, column=2)

        #Wing span field entry
        wingSpanLabel.grid(row=5, column=1, padx=10)
        wingSpanInput.grid(row=5, column=2)

        #Length field entry
        vLengthLabel.grid(row=6,column=1, padx=10) 
        vLengthInput.grid(row=6, column=2)

def resetAll(clicked: StringVar, tailInput: Text, lengthInput: Text, 
             wingSpanInput: Text, chordInput: Text, vTailInput: Text,
             vLengthInput: Text, wingInput: Text) -> None:
    '''This function clears all input boxes'''
    if(clicked.get()=="Horizontal"):
        tailInput.delete(0,"end")
        lengthInput.delete(0,"end")
        wingSpanInput.delete(0,"end")
        chordInput.delete(0,"end")
    elif(clicked.get()=="Vertical"):
        vTailInput.delete(0,"end")
        wingSpanInput.delete(0,"end")
        vLengthInput.delete(0,"end")
    wingInput.delete(0, "end")

def clearOutput(outputBox: Text) -> None:
    outputBox.configure(state=NORMAL)
    outputBox.delete("1.0", "end")
    outputBox.configure(state=DISABLED)

def setValues(clicked: StringVar, outputBox: Text,
              wingInput, chordInput, tailInput, lengthInput,
              vTailInput, vLengthInput, wingSpanInput) -> bool:
    '''This function takes user entered values from the input boxes
    and assigns to vars for ease of calculations. Returns boolean that
    is True when the values are correctly set, and False otherwise.
    '''
    try:
        if(clicked.get()=="Horizontal"):
            obj.wingArea = float(wingInput.get())
            obj.chord = float(chordInput.get())
            obj.tailArea = float(tailInput.get())
            obj.myLength = float(lengthInput.get())

            if(obj.wingArea<0 or obj.chord<0 or obj.tailArea<0 or obj.myLength<0):
                addError(outputBox, "Values cannot be negative")
                return False
        if(clicked.get()=="Vertical"):
            obj.vTailArea = float(vTailInput.get())
            obj.vLength = float(vLengthInput.get())
            obj.wingSpan = float(wingSpanInput.get())
            obj.wingArea = float(wingInput.get())

            if(obj.vTailArea<0 or obj.vLength<0 or obj.wingSpan<0 or obj.wingArea<0):
                addError(outputBox, "Values cannot be negative")
                return False
        return True
    except:
        return False

def addError(outputBox: Text, e: str):
    outputBox.configure(state=NORMAL)
    outputBox.tag_configure("redText", foreground="red")
    outputBox.insert("1.0", f"Error: {e}\n", "redText")
    outputBox.configure(state=DISABLED)

def addAnswer(outputBox: Text, ans: float):
    outputBox.configure(state=NORMAL, fg="black")
    ans = "%.5f" % ans #format answer to five decimal places
    outputBox.insert("1.0", str(ans)+"\n")
    outputBox.configure(state=DISABLED)

def submitAll(clicked: StringVar, outputBox: Text, wingInput: Text, chordInput: Text, tailInput: Text,
              lengthInput: Text, vTailInput: Text, vLengthInput: Text, wingSpanInput: Text) -> int:
    '''Calculates volume ratio, outputs calculation to widget, and 
    returns the volume ratio as an integer'''
    isSet = setValues(clicked, outputBox, wingInput, chordInput, tailInput, lengthInput,
              vTailInput, vLengthInput, wingSpanInput)
    if(isSet):
        try:
            if(clicked.get()=="Horizontal"):
                outputBox.configure(state=NORMAL)
                h_volumeRatio = (obj.tailArea*obj.myLength)/(obj.wingArea*obj.chord) #Calculates the volume ratio for horizontal stabilizer
                addAnswer(outputBox, h_volumeRatio)
                return h_volumeRatio
            elif(clicked.get()=="Vertical"):
                outputBox.configure(state=NORMAL)
                v_volumeRatio = (obj.vTailArea*obj.vLength)/(obj.wingArea*obj.wingSpan) #Calculates the volume ratio for vertical stabilizer
                addAnswer(outputBox, v_volumeRatio)
                return v_volumeRatio
        except ZeroDivisionError:
            addError(outputBox, "Division by Zero")
    else:
        addError(outputBox, "Incorrect Input")