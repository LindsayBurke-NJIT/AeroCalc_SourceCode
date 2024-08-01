'''Tab 1 -- Competition Score Calculator'''
from tkinter import *

def constructTab(tab1: Frame, colorSelection: str, fontName: str) -> None:
    myLabel = Label(tab1, text="SAE Aero Design Scoring Calculator\n", bg=colorSelection, font=fontName+" 15 bold", justify=CENTER).grid(row=0, column=0,columnspan=4, padx=(100,100))

    pPayLabel = Label(tab1, text="Predicted Payload (lbs)", bg=colorSelection, font=fontName+" 13 bold").grid(row=1, column=1)
    pPayInput = Entry(tab1)
    pPayInput.grid(row=1, column=2,pady=5)

    wingspanLabel = Label(tab1, text="Wingspan (ft)", bg=colorSelection, font=fontName+" 13 bold").grid(row=2, column=1)
    wingspanInput = Entry(tab1)
    wingspanInput.grid(row=2, column=2,pady=5)

    w1Label = Label(tab1, text="Cargo Weight Flight 1 (lbs)", bg=colorSelection, font=fontName+" 13 bold").grid(row=3, column=1)
    w1Input = Entry(tab1)
    w1Input.grid(row=3, column=2,pady=5)

    w2Label = Label(tab1, text="Cargo Weight Flight 2 (lbs)", bg=colorSelection, font=fontName+" 13 bold").grid(row=4, column=1)
    w2Input = Entry(tab1)
    w2Input.grid(row=4, column=2,pady=5)

    w3Label = Label(tab1, text="Cargo Weight Flight 3 (lbs)", bg=colorSelection, font=fontName+" 13 bold").grid(row=5, column=1)
    w3Input = Entry(tab1)
    w3Input.grid(row=5, column=2,pady=5)

    outputLabel = Label(tab1, text="Final Flight Score:", bg=colorSelection, font=fontName+" 13 bold").grid(row=9, column=1, columnspan=2, pady=(70, 0))
    outputBox = Text(tab1, state=DISABLED, width=20, height = 3, fg="red", wrap="word")
    outputBox.grid(row=10, column=1, columnspan=2)

    startButton = Button(tab1, text="Calculate", command=lambda: calcFS(pPayInput, wingspanInput, w1Input, w2Input, w3Input, outputBox), width=7, height=1, bg="gray", fg="black", font=fontName, relief="sunken")
    startButton.grid(row=6,column=1,columnspan=2, pady=(20,0))

def addError(outputBox: Text, e: str):
    clrError(outputBox)
    outputBox.configure(state=NORMAL, fg="red")
    outputBox.insert("1.0", (e+"\n"))
    outputBox.configure(state=DISABLED)

def calcFS(pPayInput: Entry, wingspanInput: Entry, w1Input: Entry, w2Input: Entry, w3Input: Entry, outputBox: Entry) -> bool:
    '''
    Calculates flight score for each flight
    '''
    try:
        weightList = setVals(pPayInput, wingspanInput, w1Input, w2Input, w3Input, outputBox)
        if(weightList==False):
            return False
        predictedPayload = pPayInput.get()
        wingspan = wingspanInput.get()
        wingScore = calcWS(wingspan)

        finalFs = 0
        for i in range(3):
            wvar = weightList[i]
            currFlightScore = wvar/2+setPPB(wvar, predictedPayload)
            finalFs+=currFlightScore
        finalFs+=wingScore

        clrError(outputBox)
        outputBox.configure(state=NORMAL, fg="black")
        outputBox.insert("1.0", str(finalFs)+"\n")
        outputBox.configure(state=DISABLED)
    except:
        pass

def setPPB(wvar: float, pPay: str) -> float:
    '''
    Calculates and sets payload prediction bonus
    '''
    temp_ppb=(5-((wvar-float(pPay))**2)) 
    return 0 if(temp_ppb<0) else temp_ppb

def clrError(outputBox: Text):
    outputBox.configure(state=NORMAL, fg="red")
    outputBox.delete("1.0", END)
    outputBox.configure(state=DISABLED)

def calcWS(wingspan: str) -> float:
    return 2**(1+float(wingspan)/5)

def setVals(pPayInput: Entry, wingspanInput: Entry, w1Input: Entry, w2Input: Entry, w3Input: Entry, outputBox: Text) -> tuple[float] | bool:
    '''
    Sets values of calculation vars from input boxes.
    If the values are valid, the function returns a tuple of the weight entries.
    If they are invalid, the function returns False
    '''
    try:
        pPay = float(pPayInput.get())
        wingspan = float(wingspanInput.get())
        w1 = float(w1Input.get())
        w2 = float(w2Input.get())
        w3 = float(w3Input.get())
        if(pPay<0 or wingspan<0 or w1<0 or w2<0 or w3<0):
            addError(outputBox, "Values cannot be negative\n")
            return False
        return (w1, w2, w3)
    except:
        addError(outputBox, "Please enter numerical values only\n")
        return False