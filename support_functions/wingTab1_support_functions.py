"""Tab 1 -- Aspect/Taper Ratio"""
from tkinter import *

def constructTab(tab2: Frame, colorSelection: str, fontName: str) -> None:
    '''Creates all of the Tkinter widgets'''
    #Defines all labels, buttons, and input boxes
    ttlLabel = Label(tab2, text="Aspect Ratio, Area, and Taper Ratio Calculator\n", bg=colorSelection, font=fontName+" 15 bold", justify=CENTER).grid(row=0, column=0,columnspan=4, padx=(40,52))
    tipChordLabel = Label(tab2, text="Tip Chord", bg=colorSelection, font=fontName+" 13 bold").grid(row=1, column=1)
    tipChordInput = Entry(tab2)
    tipChordInput.grid(row=1, column=2)

    rootChordLabel = Label(tab2, text="Root Chord", bg=colorSelection, font=fontName+" 13 bold").grid(row=2, column=1)
    rootChordInput = Entry(tab2)
    rootChordInput.grid(row=2, column=2)

    spanLabel = Label(tab2, text="Span 1 (constant-chord span)", bg=colorSelection, font=fontName+" 13 bold").grid(row=3, column=1)
    spanInput = Entry(tab2)
    spanInput.grid(row=3, column=2)

    span2Label = Label(tab2, text="Span 2 (wingtip to end of taper)", bg=colorSelection, font=fontName+" 13 bold").grid(row=4, column=1)
    span2Input = Entry(tab2)
    span2Input.grid(row=4, column=2)

    areaLabel = Label(tab2, text="Wing Area", bg=colorSelection, font=fontName+" 13 bold").grid(row=6, column=1)
    areaInput = Text(tab2, state=DISABLED, width=15, height=1)
    areaInput.grid(row=6, column=2)

    aspectLabel = Label(tab2, text="Aspect Ratio", bg=colorSelection, font=fontName+" 13 bold").grid(row=7, column=1)
    aspectInput = Text(tab2, state=DISABLED, width=15, height=1)
    aspectInput.grid(row=7, column=2)

    taperLabel = Label(tab2, text="Taper Ratio", bg=colorSelection, font=fontName+" 13 bold").grid(row=8, column=1)
    taperInput = Text(tab2, state=DISABLED, width=15, height=1)
    taperInput.grid(row=8, column=2)

    errorLabel = Label(tab2, text="Error Log", bg=colorSelection, font=fontName+" 13 bold").grid(row=9, column=1, columnspan=2, pady=(40, 0))
    errorInput = Text(tab2, state=DISABLED, width=20, height = 5, fg="red", wrap="word")
    errorInput.grid(row=10, column=1, columnspan=2)

    startButton2 = Button(tab2, text="Calculate", command=lambda: calcAll(tipChordInput, rootChordInput, spanInput, span2Input, errorInput, areaInput, taperInput, aspectInput), width=7, height=1, bg="cornflowerblue", font=fontName, relief="sunken")
    startButton2.grid(row=5,column=1,columnspan=2, pady=(5,60))
 
def setVals(tipChordInput: Text, rootChordInput: Text, spanInput: Text, span2Input: Text, errorInput: Text) -> bool:
    '''This function sets the values of variables from input boxes
        It returns true if the values were correctly set, and false otherwise.
    '''
    global rtChord, tipChord, span1, span2

    try:
        tipChord = float(tipChordInput.get())
        span1 = float(spanInput.get())
        span2 = float(span2Input.get())
        rtChord = float(rootChordInput.get())
        if(tipChord<0 or span1<0 or span2<0 or rtChord<0):
            errorInput.configure(state=NORMAL)
            errorInput.insert("1.0", "Cannot enter negative values\n")
            errorInput.configure(state=DISABLED)
            return False
        if(rtChord==0):
            errorInput.configure(state=NORMAL)
            errorInput.insert("1.0", "Root chord cannot be zero\n")
            errorInput.configure(state=DISABLED)
            return False
        return True
    except ValueError:
        errorInput.configure(state=NORMAL)
        errorInput.insert("1.0", "Please enter numerical values only\n")
        errorInput.configure(state=DISABLED)
    except TypeError:
        errorInput.configure(state=NORMAL)
        errorInput.insert("1.0", "Please enter numerical values only\n")
        errorInput.configure(state=DISABLED)
    return False

def calcArea(areaInput: Text) -> int:
    '''Calculates area and returns it as an integer'''
    global area

    try:
        areaInput.configure(state=NORMAL)
        area = (span1*rtChord+span2*(tipChord+rtChord)) #Calculates area
        area = float("%.3f" % area)
        areaInput.insert("1.0", str(area)+"\n")
        areaInput.configure(state=DISABLED)
        return area
    except NameError:
        return -1

def calcAsptRatio(aspectInput: Text, errorInput: Text) -> int:
    '''Calculates aspect ratio and returns it as an integer'''
    try:
        aspectInput.configure(state=NORMAL)
        tspan = span1+span2*2 #total wingspan
        asptRatio = ((tspan**2)/area) #calculates aspect ratio
        asptRatio = float("%.5f" % asptRatio)
        aspectInput.insert("1.0", str(asptRatio)+"\n")
        aspectInput.configure(state=DISABLED)
        return asptRatio
    except ZeroDivisionError:
        errorInput.configure(state=NORMAL)
        errorInput.insert("1.0", "Area cannot be zero.\n")
        errorInput.configure(state=DISABLED)
    except NameError:
        pass
    return -1

def calcTprRatio(taperInput: Text, errorInput: Text) -> int:
    '''Calculates taper ratio and returns it as an integer'''
    try:
        taperInput.configure(state=NORMAL)
        tprRatio = (tipChord/rtChord) #Calculates taper ratio
        tprRatio = float("%.5f" % tprRatio)
        taperInput.insert("1.0", str(tprRatio)+"\n")
        taperInput.configure(state=DISABLED)
        return tprRatio
    except ZeroDivisionError:
        errorInput.configure(state=NORMAL)
        errorInput.insert("1.0", "Root chord cannot be zero.\n")
        errorInput.configure(state=DISABLED)
    except NameError:
        pass
    return -1

def clearError(errorInput: Text) -> None:
    '''Clear the error output'''
    errorInput.configure(state=NORMAL)
    errorInput.delete("1.0", END)
    errorInput.configure(state=DISABLED)

def clearOutput(areaBox: Text, aspectBox: Text, taperBox: Text) -> None:
    boxesToClear = [areaBox, aspectBox, taperBox]
    for box in boxesToClear:
        box.configure(state=NORMAL)
        box.delete("1.0", END)
        box.configure(state=DISABLED)

def calcAll(tipChordInput: Text, rootChordInput: Text, spanInput: Text, span2Input: Text, errorInput: Text,
            areaInput: Text, taperInput: Text, aspectInput: Text) -> None:
    '''Calculates all variables when the Calculate button is selected'''
    clearError(errorInput)
    clearOutput(areaInput, aspectInput, taperInput)

    isSet = setVals(tipChordInput, rootChordInput, spanInput, span2Input, errorInput)
    if(isSet):
        calcArea(areaInput)
        calcAsptRatio(aspectInput, errorInput)
        calcTprRatio(taperInput, errorInput)