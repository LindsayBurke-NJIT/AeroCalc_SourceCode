'''Tab 2 -- Takeoff Distance'''
from tkinter import *
import math

def constructTab(tab: Frame, bgColor: str, font: str) -> None:
    '''Creates all of the Tkinter widgets for takeoff distance calculation using Runge-Kutta method'''
    # Configure grid weights for responsive layout
    tab.rowconfigure(15, weight=1)  # Make error input expandable
    tab.columnconfigure(0, weight=1)  # Left margin
    tab.columnconfigure(3, weight=1)  # Right margin
    
    # Title
    ttlLabel = Label(tab, text="Takeoff Distance Calculator (Runge-Kutta Method)\n", bg=bgColor, font=font+" 15 bold", justify=CENTER)
    ttlLabel.grid(row=0, column=0, columnspan=4, padx=(40, 52), pady=10)
    
    # Aircraft Mass
    massLabel = Label(tab, text="Aircraft Mass (kg)", bg=bgColor, font=font+" 13 bold")
    massLabel.grid(row=1, column=1, pady=5, sticky='w')
    massInput = Entry(tab)
    massInput.grid(row=1, column=2, pady=5)
    
    # Thrust
    thrustLabel = Label(tab, text="Thrust (N)", bg=bgColor, font=font+" 13 bold")
    thrustLabel.grid(row=2, column=1, pady=5, sticky='w')
    thrustInput = Entry(tab)
    thrustInput.grid(row=2, column=2, pady=5)
    
    # Wing Area
    wingAreaLabel = Label(tab, text="Wing Area (m²)", bg=bgColor, font=font+" 13 bold")
    wingAreaLabel.grid(row=3, column=1, pady=5, sticky='w')
    wingAreaInput = Entry(tab)
    wingAreaInput.grid(row=3, column=2, pady=5)
    
    # Lift Coefficient
    clLabel = Label(tab, text="Lift Coefficient (CL)", bg=bgColor, font=font+" 13 bold")
    clLabel.grid(row=4, column=1, pady=5, sticky='w')
    clInput = Entry(tab)
    clInput.grid(row=4, column=2, pady=5)
    
    # Drag Coefficient
    cdLabel = Label(tab, text="Drag Coefficient (CD)", bg=bgColor, font=font+" 13 bold")
    cdLabel.grid(row=5, column=1, pady=5, sticky='w')
    cdInput = Entry(tab)
    cdInput.grid(row=5, column=2, pady=5)
    
    # Air Density
    rhoLabel = Label(tab, text="Air Density (kg/m³)", bg=bgColor, font=font+" 13 bold")
    rhoLabel.grid(row=6, column=1, pady=5, sticky='w')
    rhoInput = Entry(tab)
    rhoInput.insert(0, "1.225")  # Default sea level density
    rhoInput.grid(row=6, column=2, pady=5)
    
    # Rolling Friction Coefficient
    muLabel = Label(tab, text="Rolling Friction Coefficient (μ)", bg=bgColor, font=font+" 13 bold")
    muLabel.grid(row=7, column=1, pady=5, sticky='w')
    muInput = Entry(tab)
    muInput.insert(0, "0.02")  # Default for typical aircraft tires
    muInput.grid(row=7, column=2, pady=5)
    
    # Rotation Speed
    vRotLabel = Label(tab, text="Rotation Speed (m/s)", bg=bgColor, font=font+" 13 bold")
    vRotLabel.grid(row=8, column=1, pady=5, sticky='w')
    vRotInput = Entry(tab)
    vRotInput.grid(row=8, column=2, pady=5)
    
    # Time Step for Runge-Kutta
    dtLabel = Label(tab, text="Time Step (s)", bg=bgColor, font=font+" 13 bold")
    dtLabel.grid(row=9, column=1, pady=5, sticky='w')
    dtInput = Entry(tab)
    dtInput.insert(0, "0.01")  # Default 0.01 seconds
    dtInput.grid(row=9, column=2, pady=5)
    
    # Calculate button
    calcButton = Button(tab, text="Calculate", command=lambda: calcTakeoffDistance(massInput, thrustInput, wingAreaInput, clInput, cdInput, rhoInput, muInput, vRotInput, dtInput, distanceOutput, errorInput), width=7, height=1, bg="cornflowerblue", font=font, relief="sunken")
    calcButton.grid(row=10, column=1, columnspan=2, pady=(10, 20))
    
    # Output - Takeoff Distance
    distanceLabel = Label(tab, text="Takeoff Distance (m)", bg=bgColor, font=font+" 13 bold")
    distanceLabel.grid(row=11, column=1, pady=5, sticky='w')
    distanceOutput = Text(tab, state=DISABLED, width=15, height=1)
    distanceOutput.grid(row=11, column=2, pady=5)
    
    # Error log
    errorLabel = Label(tab, text="Error Log", bg=bgColor, font=font+" 13 bold")
    errorLabel.grid(row=12, column=1, columnspan=2, pady=(40, 0))
    errorInput = Text(tab, state=DISABLED, width=30, height=5, fg="red", wrap="word")
    errorInput.grid(row=13, column=1, columnspan=2)


def setVals(massInput: Entry, thrustInput: Entry, wingAreaInput: Entry, clInput: Entry, cdInput: Entry, rhoInput: Entry, muInput: Entry, vRotInput: Entry, dtInput: Entry, errorInput: Text) -> bool:
    '''This function sets the values of variables from input boxes
    It returns true if the values were correctly set, and false otherwise.
    '''
    global mass, thrust, wingArea, cl, cd, rho, mu, vRot, dt
    
    try:
        mass = float(massInput.get())
        thrust = float(thrustInput.get())
        wingArea = float(wingAreaInput.get())
        cl = float(clInput.get())
        cd = float(cdInput.get())
        rho = float(rhoInput.get())
        mu = float(muInput.get())
        vRot = float(vRotInput.get())
        dt = float(dtInput.get())
        
        # Validate positive values
        if mass <= 0 or thrust <= 0 or wingArea <= 0 or rho <= 0 or dt <= 0:
            addError(errorInput, "ERROR: Mass, Thrust, Wing Area, Air Density, and Time Step must be positive.")
            return False
        
        if vRot < 0:
            addError(errorInput, "ERROR: Rotation speed cannot be negative.")
            return False
        
        if dt > 1.0:
            addError(errorInput, "ERROR: Time step should be small (recommended < 0.1 s) for accurate results.")
            return False
        
        return True
    except ValueError:
        addError(errorInput, "ERROR: Invalid input. Please ensure all fields contain valid numbers.")
        return False


def acceleration(v: float, mass: float, thrust: float, wingArea: float, cl: float, cd: float, rho: float, mu: float) -> float:
    '''Calculate acceleration at current velocity using F = ma
    Forces: Thrust - Drag - Friction - Lift (vertical component on ground)
    On ground, lift reduces normal force, thus reducing friction
    '''
    # Dynamic pressure
    q = 0.5 * rho * v * v
    
    # Lift and Drag forces
    lift = cl * wingArea * q
    drag = cd * wingArea * q
    
    # Normal force on ground (mg - lift)
    gravity = 9.81
    normalForce = mass * gravity - lift
    
    # Friction force (can't be negative)
    friction = mu * max(0, normalForce)
    
    # Net force = Thrust - Drag - Friction
    netForce = thrust - drag - friction
    
    # Acceleration
    a = netForce / mass
    
    return a


def rungeKuttaStep(v: float, mass: float, thrust: float, wingArea: float, cl: float, cd: float, rho: float, mu: float, dt: float) -> float:
    '''One step of 4th order Runge-Kutta method for dv/dt = acceleration'''
    k1 = acceleration(v, mass, thrust, wingArea, cl, cd, rho, mu) * dt
    k2 = acceleration(v + k1/2, mass, thrust, wingArea, cl, cd, rho, mu) * dt
    k3 = acceleration(v + k2/2, mass, thrust, wingArea, cl, cd, rho, mu) * dt
    k4 = acceleration(v + k3, mass, thrust, wingArea, cl, cd, rho, mu) * dt
    
    v_new = v + (k1 + 2*k2 + 2*k3 + k4) / 6
    return max(0, v_new)  # Velocity can't be negative


def calcTakeoffDistance(massInput: Entry, thrustInput: Entry, wingAreaInput: Entry, clInput: Entry, cdInput: Entry, rhoInput: Entry, muInput: Entry, vRotInput: Entry, dtInput: Entry, distanceOutput: Text, errorInput: Text) -> bool:
    '''Calculate takeoff distance using Runge-Kutta method'''
    
    if not setVals(massInput, thrustInput, wingAreaInput, clInput, cdInput, rhoInput, muInput, vRotInput, dtInput, errorInput):
        clrOutput(distanceOutput)
        return False
    
    try:
        clrError(errorInput)
        clrOutput(distanceOutput)
        
        # Initial conditions
        v = 0.0  # Initial velocity
        distance = 0.0  # Initial distance
        maxIterations = 100000  # Safety limit
        iteration = 0
        
        # If rotation speed is 0, calculate until aircraft lifts off (when lift = weight)
        if vRot <= 0:
            # Find lift-off speed (when lift = weight)
            gravity = 9.81
            vRot = math.sqrt(2 * mass * gravity / (cl * rho * wingArea))
        
        # Integrate until rotation speed is reached
        while v < vRot and iteration < maxIterations:
            # Calculate distance in this time step (using average velocity)
            v_old = v
            v = rungeKuttaStep(v, mass, thrust, wingArea, cl, cd, rho, mu, dt)
            distance += (v_old + v) / 2 * dt  # Trapezoidal integration for distance
            iteration += 1
        
        if iteration >= maxIterations:
            addError(errorInput, "WARNING: Maximum iterations reached. Aircraft may not reach rotation speed with given parameters.")
        
        # Display result
        distanceOutput.configure(state=NORMAL)
        distanceOutput.insert("1.0", f"{distance:.2f} m")
        distanceOutput.configure(state=DISABLED)
        
        return True
    except Exception as e:
        addError(errorInput, f"ERROR: Calculation failed - {str(e)}")
        clrOutput(distanceOutput)
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
