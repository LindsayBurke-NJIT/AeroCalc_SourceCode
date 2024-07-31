"""Tab1 -- Volume Ratio"""
from tkinter import *

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
    chordLabel = Label(tab1, text="Mean Aerodynamic \nChord", bg=colorSelection,  highlightcolor=colorSelection, highlightbackground=colorSelection, highlightthickness=bgThickness, font=fontName+" 12 bold")
    chordLabel.grid(row=4,column=1, padx=10) 
    chordInput = Entry(tab1)
    chordInput.grid(row=4, column=2)
            
    #Horizontal tail area field entry
    tailLabel = Label(tab1, text="Horizontal Tail \nArea", bg=colorSelection, highlightcolor=colorSelection, highlightbackground=colorSelection, highlightthickness=bgThickness, font=fontName+" 12 bold")
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
    outputLabel.grid(row=8, column=2, pady=(10,0))
    outputBox = Text(tab1, width=20, height=5, font=fontName+" 13")
    outputBox.grid(row=9, column=2, padx=(10,0), sticky='w')
    outputBox.configure(state=DISABLED)

    #Defines all buttons
    dropButton = Button(tab1, text="Select", command=lambda: submitDrop(tab1, clicked, colorSelection, fontName, bgThickness, outputBox,
                                                                        chordLabel, chordInput, tailLabel, tailInput, lengthLabel, lengthInput,
                                                                        vTailLabel, vTailInput, wingSpanLabel, wingSpanInput, vLengthLabel, vLengthInput), 
                                                                        width=6, height=1, bg="cornflowerblue", font=fontName+" 8")
    dropButton.grid(row=2, column=2, columnspan=2)

    startButton = Button(tab1, text="Calculate", command=lambda: submitAll(clicked, outputBox, wingInput, 
                                                                           chordInput, tailInput, lengthInput, 
                                                                           vTailInput, vLengthInput, wingSpanInput),
                                                                           width=7, height=2, bg="greenyellow", 
                                                                           font=fontName, relief="sunken")
    startButton.grid(sticky='nw', row=9, column=1, padx=(23,0))

    resetButton = Button(tab1, text="Clear \nInput", command=lambda: resetAll(clicked, tailInput, lengthInput, wingSpanInput, chordInput, vTailInput, vLengthInput, wingInput), width=7, height=2, bg="cornflowerblue", font=fontName, relief="sunken")
    resetButton.grid(sticky="ne", row=9, column=1)

    clearOutputButton = Button(tab1, text="Clear \nOutput", command=lambda: clearOutput(outputBox), width=7, height=2, bg="cornflowerblue", font=fontName, relief="sunken")
    clearOutputButton.grid(sticky='n', row=9, column=1, padx=(13,0))

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
    try:
        if(clicked.get()=="Horizontal"):
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
            #Vertical wing area field entry
            vTailLabel.grid(row=4,column=1, padx=10)
            vTailInput.grid(row=4, column=2)

            #Wing span field entry
            wingSpanLabel.grid(row=5, column=1, padx=10)
            wingSpanInput.grid(row=5, column=2)

            #Length field entry
            vLengthLabel.grid(row=6,column=1, padx=10) 
            vLengthInput.grid(row=6, column=2)
    except NameError:
        outputBox.configure(state=NORMAL)
        outputBox.insert("1.0", "Error: Incorrect entry\n")
        outputBox.configure(state=DISABLED)

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
              vTailInput, vLengthInput, wingSpanInput):
    '''This function takes user entered values from the input boxes
    and assigns to vars for ease of calculations
    '''
    try:
        global wingArea,chord,tailArea,myLength,vTailArea,vLength,wingSpan
        if(clicked.get()=="Horizontal"):
            wingArea = float(wingInput.get())
            chord = float(chordInput.get())
            tailArea = float(tailInput.get())
            myLength = float(lengthInput.get())
        if(clicked.get()=="Vertical"):
            vTailArea = float(vTailInput.get())
            vLength = float(vLengthInput.get())
            wingSpan = float(wingSpanInput.get())
            wingArea = float(wingInput.get())
    except ValueError:
        outputBox.configure(state=NORMAL)
        outputBox.insert("1.0", "Error: Value is invalid.\n")
        outputBox.configure(state=DISABLED)

def submitAll(clicked: StringVar, outputBox: Text, wingInput: Text, chordInput: Text, tailInput: Text,
              lengthInput: Text, vTailInput: Text, vLengthInput: Text, wingSpanInput: Text) -> int:
    '''Calculates volume ratio, outputs calculation to widget, and 
    returns the volume ratio as an integer'''
    setValues(clicked, outputBox, wingInput, chordInput, tailInput, lengthInput,
              vTailInput, vLengthInput, wingSpanInput)
    try:
        if(clicked.get()=="Horizontal"):
            outputBox.configure(state=NORMAL)
            h_volumeRatio = (tailArea*myLength)/(wingArea*chord) #Calculates the volume ratio for horizontal stabilizer
            outputBox.insert("1.0", str(h_volumeRatio) + '\n')
            outputBox.configure(state=DISABLED)
            return h_volumeRatio
        elif(clicked.get()=="Vertical"):
            outputBox.configure(state=NORMAL)
            v_volumeRatio = (vTailArea*vLength)/(wingArea*wingSpan) #Calculates the volume ratio for vertical stabilizer
            outputBox.insert("1.0", str(v_volumeRatio) + '\n')
            outputBox.configure(state=DISABLED)
            return v_volumeRatio
    except ZeroDivisionError:
        outputBox.configure(state=NORMAL)
        outputBox.insert("1.0", "Error: Division by Zero\n")
        outputBox.configure(state=DISABLED)
    except ValueError:
        outputBox.configure(state=NORMAL)
        outputBox.insert("1.0", "Error: Incorrect entry\n")
        outputBox.configure(state=DISABLED)
    except NameError:
        outputBox.configure(state=NORMAL)
        outputBox.insert("1.0", "Error: Incorrect entry\n")
        outputBox.configure(state=DISABLED)