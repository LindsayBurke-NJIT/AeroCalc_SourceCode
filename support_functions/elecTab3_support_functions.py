"""Tab 3 -- Voltage Drop Calculator"""
from tkinter import *


def evaluateMathExpression(expr: str) -> float:
    '''Evaluate mathematical expressions like "1.28*10^-7" or "2.5*10**-6"
    Converts ^ to ** (Python exponentiation) and evaluates the expression'''
    try:
        # Replace ^ with ** for Python exponentiation
        expr = expr.replace('^', '**')
        # Evaluate the expression
        result = eval(expr, {"__builtins__": {}}, {})
        return float(result)
    except Exception as e:
        raise ValueError(f"Cannot evaluate expression: {expr}")

def constructTab(tab3: Frame, colorSelection: str, fontName: str) -> None:
    '''Creates all of the Tkinter widgets for voltage drop calculation'''
    # Configure grid weights for responsive layout
    tab3.rowconfigure(6, weight=1)  # Make error input expandable
    tab3.columnconfigure(0, weight=1)  # Left margin
    tab3.columnconfigure(3, weight=1)  # Right margin
    
    # Title
    ttlLabel = Label(tab3, text="Voltage Drop Calculator\n", bg=colorSelection, font=fontName+" 15 bold", justify=CENTER)
    ttlLabel.grid(row=0, column=0, columnspan=4, padx=(40, 52))
    
    # Wire Length input
    wireLengthLabel = Label(tab3, text="Wire Length (m)", bg=colorSelection, font=fontName+" 13 bold")
    wireLengthLabel.grid(row=1, column=1, pady=5)
    wireLengthInput = Entry(tab3)
    wireLengthInput.grid(row=1, column=2, pady=5)
    
    # Cross-sectional Area input
    areaLabel = Label(tab3, text="Cross-sectional Area of Wire (m²)", bg=colorSelection, font=fontName+" 13 bold")
    areaLabel.grid(row=2, column=1, pady=5)
    areaInput = Entry(tab3)
    areaInput.grid(row=2, column=2, pady=5)
    
    # Max Amperage Draw per Servo input
    amperageLabel = Label(tab3, text="Max Amperage Draw per Servo (A)", bg=colorSelection, font=fontName+" 13 bold")
    amperageLabel.grid(row=3, column=1, pady=5)
    amperageInput = Entry(tab3)
    amperageInput.grid(row=3, column=2, pady=5)
    
    # Calculate button
    calcButton = Button(tab3, text="Calculate", command=lambda: calcVoltageDrop(wireLengthInput, areaInput, amperageInput, voltageOutput, errorInput), width=7, height=1, bg="cornflowerblue", font=fontName, relief="sunken")
    calcButton.grid(row=4, column=1, columnspan=2, pady=(10, 20))
    
    # Output - Voltage Drop
    voltageLabel = Label(tab3, text="Voltage Drop (V)", bg=colorSelection, font=fontName+" 13 bold")
    voltageLabel.grid(row=5, column=1, pady=5)
    voltageOutput = Text(tab3, state=DISABLED, width=15, height=1)
    voltageOutput.grid(row=5, column=2, pady=5)
    
    # Error log
    errorLabel = Label(tab3, text="Error Log", bg=colorSelection, font=fontName+" 13 bold")
    errorLabel.grid(row=6, column=1, columnspan=2, pady=(40, 0))
    errorInput = Text(tab3, state=DISABLED, width=20, height=5, fg="red", wrap="word")
    errorInput.grid(row=7, column=1, columnspan=2)


def setVals(wireLengthInput: Entry, areaInput: Entry, amperageInput: Entry, errorInput: Text) -> bool:
    '''This function sets the values of variables from input boxes
    It returns true if the values were correctly set, and false otherwise.
    Supports mathematical expressions like "1.28*10^-7" for cross-sectional area.
    '''
    global wireLength, crossSectionalArea, amperageDraw
    
    try:
        wireLengthStr = wireLengthInput.get().strip()
        areaStr = areaInput.get().strip()
        amperageStr = amperageInput.get().strip()
        
        # Try to evaluate wire length and amperage as regular numbers first
        try:
            wireLength = float(wireLengthStr)
        except ValueError:
            wireLength = evaluateMathExpression(wireLengthStr)
        
        # Cross-sectional area can be a mathematical expression (like 1.28*10^-7)
        try:
            crossSectionalArea = float(areaStr)
        except ValueError:
            crossSectionalArea = evaluateMathExpression(areaStr)
        
        try:
            amperageDraw = float(amperageStr)
        except ValueError:
            amperageDraw = evaluateMathExpression(amperageStr)
        
        # Validate positive values
        if wireLength <= 0 or crossSectionalArea <= 0 or amperageDraw <= 0:
            addError(errorInput, "ERROR: All values must be positive and non-zero.")
            return False
        
        return True
    except (ValueError, SyntaxError) as e:
        addError(errorInput, f"ERROR: Invalid input. Please ensure all fields contain valid numbers or expressions.\n(e.g., 1.28*10^-7 for scientific notation)")
        return False


def calcVoltageDrop(wireLengthInput: Entry, areaInput: Entry, amperageInput: Entry, voltageOutput: Text, errorInput: Text) -> bool:
    '''Calculate the voltage drop using the provided formula'''
    
    if not setVals(wireLengthInput, areaInput, amperageInput, errorInput):
        clrOutput(voltageOutput)
        return False
    
    try:
        clrError(errorInput)
        clrOutput(voltageOutput)
        
        # Calculate total resistance
        # resistivity of copper = 1.72 * 10^-8 Ω·m
        resistivity = 1.72e-8
        totalResistance = resistivity * wireLength / crossSectionalArea
        
        # Calculate voltage drop
        # Formula: 2 * totalResistance * totalAmpDrawPerServo * WireLength
        voltageDrop = 2 * totalResistance * amperageDraw * wireLength
        
        # Display result
        voltageOutput.configure(state=NORMAL)
        voltageOutput.insert("1.0", f"{voltageDrop:.6f} V")
        voltageOutput.configure(state=DISABLED)
        
        return True
    except Exception as e:
        addError(errorInput, f"ERROR: Calculation failed - {str(e)}")
        clrOutput(voltageOutput)
        return False


def addError(errorBox: Text, e: str) -> None:
    '''Add error message to error log'''
    clrError(errorBox)
    errorBox.configure(state=NORMAL, fg="red")
    errorBox.insert("1.0", (e + "\n"))
    errorBox.configure(state=DISABLED)


def clrError(errorBox: Text) -> None:
    '''Clear error log'''
    errorBox.configure(state=NORMAL)
    errorBox.delete("1.0", END)
    errorBox.configure(state=DISABLED)


def clrOutput(outputBox: Text) -> None:
    '''Clear output box'''
    outputBox.configure(state=NORMAL)
    outputBox.delete("1.0", END)
    outputBox.configure(state=DISABLED)
