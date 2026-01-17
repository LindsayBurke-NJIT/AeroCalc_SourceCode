"""Tab 2 -- Servo Torque Calculator"""
from tkinter import *
import math

def constructTab(tab2: Frame, colorSelection: str, fontName: str) -> None:
    '''Creates all of the Tkinter widgets for servo torque calculation'''
    # Configure grid weights for responsive layout
    tab2.rowconfigure(11, weight=1)  # Make error input expandable
    tab2.columnconfigure(0, weight=1)  # Left margin
    tab2.columnconfigure(3, weight=1)  # Right margin
    
    # Title
    ttlLabel = Label(tab2, text="Servo Torque Calculator\n", bg=colorSelection, font=fontName+" 15 bold", justify=CENTER)
    ttlLabel.grid(row=0, column=0, columnspan=4, padx=(40, 52))
    
    # Chord input
    chordLabel = Label(tab2, text="Chord (inches)", bg=colorSelection, font=fontName+" 13 bold")
    chordLabel.grid(row=1, column=1)
    chordInput = Entry(tab2)
    chordInput.grid(row=1, column=2)
    
    # Length input
    lengthLabel = Label(tab2, text="Length (inches)", bg=colorSelection, font=fontName+" 13 bold")
    lengthLabel.grid(row=2, column=1)
    lengthInput = Entry(tab2)
    lengthInput.grid(row=2, column=2)
    
    # Aircraft speed input
    speedLabel = Label(tab2, text="Aircraft Speed (mph)", bg=colorSelection, font=fontName+" 13 bold")
    speedLabel.grid(row=3, column=1)
    speedInput = Entry(tab2)
    speedInput.grid(row=3, column=2)
    
    # Control surface deflection input
    csDeflLabel = Label(tab2, text="CS Deflection (degrees)", bg=colorSelection, font=fontName+" 13 bold")
    csDeflLabel.grid(row=4, column=1)
    csDeflInput = Entry(tab2)
    csDeflInput.grid(row=4, column=2)
    
    # Servo deflection input
    servDeflLabel = Label(tab2, text="Servo Deflection (degrees)", bg=colorSelection, font=fontName+" 13 bold")
    servDeflLabel.grid(row=5, column=1)
    servDeflInput = Entry(tab2)
    servDeflInput.grid(row=5, column=2)
    
    # Factor of Safety input
    fosLabel = Label(tab2, text="Factor of Safety (%)", bg=colorSelection, font=fontName+" 13 bold")
    fosLabel.grid(row=6, column=1)
    fosInput = Entry(tab2)
    fosInput.grid(row=6, column=2)
    
    # Calculate button
    calcButton = Button(tab2, text="Calculate", command=lambda: calcServoTorque(chordInput, lengthInput, speedInput, csDeflInput, servDeflInput, fosInput, torqueOutput, maxTorqueOutput, errorInput), width=7, height=1, bg="cornflowerblue", font=fontName, relief="sunken")
    calcButton.grid(row=7, column=1, columnspan=2, pady=(5, 20))
    
    # Output - Servo Torque
    torqueLabel = Label(tab2, text="Servo Torque", bg=colorSelection, font=fontName+" 13 bold")
    torqueLabel.grid(row=8, column=1)
    torqueOutput = Text(tab2, state=DISABLED, width=15, height=1)
    torqueOutput.grid(row=8, column=2)
    
    # Output - Maximum Servo Torque (with FOS)
    maxTorqueLabel = Label(tab2, text="Maximum Servo Torque (with FOS)", bg=colorSelection, font=fontName+" 13 bold")
    maxTorqueLabel.grid(row=9, column=1)
    maxTorqueOutput = Text(tab2, state=DISABLED, width=15, height=1)
    maxTorqueOutput.grid(row=9, column=2)
    
    # Error log
    errorLabel = Label(tab2, text="Error Log", bg=colorSelection, font=fontName+" 13 bold")
    errorLabel.grid(row=10, column=1, columnspan=2, pady=(40, 0))
    errorInput = Text(tab2, state=DISABLED, width=20, height=5, fg="red", wrap="word")
    errorInput.grid(row=11, column=1, columnspan=2)


def setVals(chordInput: Entry, lengthInput: Entry, speedInput: Entry, csDeflInput: Entry, servDeflInput: Entry, fosInput: Entry, errorInput: Text) -> bool:
    '''This function sets the values of variables from input boxes
    It returns true if the values were correctly set, and false otherwise.
    '''
    global chord, length, speed, csDefl, servDefl, fos
    
    try:
        chord = float(chordInput.get())
        length = float(lengthInput.get())
        speed = float(speedInput.get())
        csDefl = float(csDeflInput.get())
        servDefl = float(servDeflInput.get())
        fos = float(fosInput.get())
        
        # Validate positive values
        if chord <= 0 or length <= 0 or speed <= 0 or csDefl == 0 or servDefl == 0:
            addError(errorInput, "ERROR: All values must be non-zero. Speed, chord, and length must be positive.")
            return False
        
        # Validate factor of safety
        if fos < 0:
            addError(errorInput, "ERROR: Factor of Safety cannot be negative.")
            return False
        
        return True
    except ValueError:
        addError(errorInput, "ERROR: Invalid input. Please ensure all fields contain valid numbers.")
        return False


def calcServoTorque(chordInput: Entry, lengthInput: Entry, speedInput: Entry, csDeflInput: Entry, servDeflInput: Entry, fosInput: Entry, torqueOutput: Text, maxTorqueOutput: Text, errorInput: Text) -> bool:
    '''Calculate the servo torque required using the provided formula'''
    
    if not setVals(chordInput, lengthInput, speedInput, csDeflInput, servDeflInput, fosInput, errorInput):
        clrOutput(torqueOutput)
        clrOutput(maxTorqueOutput)
        return False
    
    try:
        clrError(errorInput)
        clrOutput(torqueOutput)
        clrOutput(maxTorqueOutput)
        
        # Convert angles to radians
        cs_defl_rad = math.radians(csDefl)
        serv_defl_rad = math.radians(servDefl)
        
        # Check for invalid angles (0 degrees for servo deflection would cause division by zero)
        if abs(servDefl) < 0.01:
            addError(errorInput, "ERROR: Servo deflection cannot be 0 or near 0 degrees.")
            return False
        
        # Formula: 8.5*(10^-6)*(Chord^2)*(Speed^2)*Length*sin(CS deflection)*tan(CS deflection)^2/tan(servo deflection)
        servo_torque = (8.5e-6 * 
                       (chord ** 2) * 
                       (speed ** 2) * 
                       length * 
                       math.sin(cs_defl_rad) * 
                       (math.tan(cs_defl_rad) ** 2) / 
                       math.tan(serv_defl_rad))
        
        # Calculate maximum servo torque with factor of safety
        # Maximum Torque = Servo Torque * (1 + FOS/100)
        max_servo_torque = abs(servo_torque) * (1 + fos / 100.0)
        
        # Display results (torque is in in-oz)
        torqueOutput.configure(state=NORMAL)
        torqueOutput.insert("1.0", f"{abs(servo_torque):.2f} in-oz")
        torqueOutput.configure(state=DISABLED)
        
        maxTorqueOutput.configure(state=NORMAL)
        maxTorqueOutput.insert("1.0", f"{max_servo_torque:.2f} in-oz")
        maxTorqueOutput.configure(state=DISABLED)
        
        return True
    except (ValueError, ZeroDivisionError) as e:
        addError(errorInput, f"ERROR: Invalid angle values. Please check your deflection angles.")
        return False
    except Exception as e:
        addError(errorInput, f"ERROR: Calculation failed - {str(e)}")
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
