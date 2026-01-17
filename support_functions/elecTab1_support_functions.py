'''Tab 1 -- automated thrust stand data visualization program'''

from tkinter import filedialog
import pandas as pd
from tkinter import *
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patch
import numpy as np

def constructTab(tab1: Frame, colorSelection:str, fontName: str) -> None:
    buttonColor = "gray"
    buttonTextColor = "black"
    
    # Configure grid weights for responsive layout
    tab1.rowconfigure(6, weight=1)  # Make ranking section expandable
    tab1.columnconfigure(0, weight=1)  # Make left margin expandable
    tab1.columnconfigure(3, weight=1)  # Make right margin expandable

    errorText = Label(tab1, text="", font=fontName, bg=colorSelection, fg="red", wraplength=450)
    errorText.grid(column=1, row=4, columnspan=5)

    fileSelectText = Label(tab1, text="Select a Folder:", font=fontName+' 15 bold', bg=colorSelection, fg=buttonTextColor)
    fileSelectText.grid(column=1, row=0, columnspan=1, padx=10, pady=10, sticky='w')

    filesToRead = [] #list of spreadsheet files in the directory that can be plotted
    maxThrust = {} #dictionary of max thrusts {fileName : maxThrust}
    maxIndices = []
    rankRows = [] #stores filenames in order of descending thrust

    fileSelectButton = Button(tab1, text="Select Folder", wraplength=400, width=40, justify=LEFT, bg=buttonColor, fg=buttonTextColor, command=lambda: selectFolder(errorText, fileSelectButton, filesToRead))
    fileSelectButton.grid(column=2, row=0, columnspan=1, padx=(10,75), pady=10, sticky='w')

    #Creates format dropdown menu
    formatOptions = ["Tyto Series 1585", "LY-10KGF"]
    formatClicked = StringVar()
    formatClicked.set("Tyto Series 1585")
    formatDropText = Label(tab1, text="Thrust Stand Model:", bg=colorSelection,font=fontName+' 15 bold')
    formatDropText.grid(row=1, column=1, pady=10, columnspan=1, sticky='w', padx=10)
    formatDropDown = OptionMenu(tab1, formatClicked, *formatOptions)
    formatDropDown.config(highlightthickness=1, bg=buttonColor, fg=buttonTextColor)
    formatDropDown.grid(row=1, column=2, columnspan=1, sticky='w', padx=10)

    #Creates thrust unit dropdown menu
    options = ["lbf", "kg"]
    clicked = StringVar()
    clicked.set("lbf")
    dropText = Label(tab1, text="Thrust Units:", bg=colorSelection,font=fontName+' 15 bold')
    dropText.grid(row=2, column=1, pady=10, columnspan=1, sticky='w', padx=10)
    unitDropDown = OptionMenu(tab1, clicked, *options)
    unitDropDown.config(highlightthickness=1, bg=buttonColor, fg=buttonTextColor)
    unitDropDown.grid(row=2, column=2, columnspan=1, sticky='w', padx=10)

    #Creates power limit entry field
    powerLimitLabel = Label(tab1, text="Power Limit (W):", bg=colorSelection, font=fontName+' 15 bold')
    powerLimitLabel.grid(row=3, column=1, pady=10, columnspan=1, sticky='w', padx=10)
    powerLimitEntry = Entry(tab1, width=15, bg="white", fg=buttonTextColor)
    powerLimitEntry.grid(row=3, column=2, columnspan=1, sticky='w', padx=10)

    startPlotButton = Button(tab1, text="Plot", width=40, bg=buttonColor, fg=buttonTextColor, command=lambda: readFiles(filesToRead, maxThrust, tab1, clicked.get(), errorText, colorSelection, maxIndices, rankRows, formatClicked.get(), powerLimitEntry))
    startPlotButton.grid(row=5, column=1, columnspan=2, pady=10, padx=(125, 0), sticky='w')

    rankingTextLabel = Label(tab1, text="Propeller Ranking:", font=fontName+" 15 bold", bg=colorSelection)
    rankingTextLabel.grid(row=6, column=1, columnspan=2, sticky='nsw', pady=20, padx=175)

def selectFolder(errorText: Label, buttonText: Button, filesToBeRead: list) -> bool:
    '''This function lets the user select a folder of xlsx/csv from a file dialogue.
    The returned value is a boolean that is True when a folder was succesfully selected, and False otherwise.'''
    global currDir

    filesToBeRead.clear() #clear filesToRead when a new folder is selected
    currDir = filedialog.askdirectory()

    try:
        for currFile in os.listdir(currDir):
            #get name and file extension from selected file
            fileParts = currFile.split(".")
            fileExtension = fileParts[-1].strip()

            if(not(fileExtension == "csv") and not(fileExtension =="xlsx")):
                continue #skip over the files that aren't spreadsheets
            else:
                filesToBeRead.append(currFile)
                buttonText.config(text=currDir, fg="black") #update label with currently selected file
                errorText.config(text="")
        if(len(filesToBeRead)==0):
            errorText.config(text="ERROR: Files in directory must be xlsx or csv. The directory cannot be empty. ")
            buttonText.config(text="Select Folder")
            return False
        #print(filesToRead)
    except:
        if currDir==None:
            errorText.config(text="ERROR: Files in directory must be xlsx or csv. The directory cannot be empty. ")
            buttonText.config(text="Select Folder")
            return False
    return True

def clearRanking(rankList: list) -> None:
    for row in range(len(rankList)):
        rankList[row].config(text="") 
    rankList.clear()

def findThrustAtPowerLimit(dataframe: pd.DataFrame, powerLimit: float, powerCol: str, thrustCol: str) -> tuple[float, float, int]:
    '''Find thrust and power at the power limit (last data point before reaching the limit)
    Returns: (thrust, power, index) or (None, None, None) if no data before limit'''
    # Filter data points where power is less than the limit (strictly before)
    filtered = dataframe[dataframe[powerCol] < powerLimit]
    if len(filtered) == 0:
        return (None, None, None)
    # Get the last index (highest power before limit)
    lastIndex = filtered.index[-1]
    thrust = filtered.iloc[-1][thrustCol]
    power = filtered.iloc[-1][powerCol]
    return (thrust, power, lastIndex)

def displayRanking(root: Frame, maxThrustList: list, rankRows: list, colorSelection: str, dropDownUnits: str, powerInWatts: dict, powerLimit: float = None):
    #Display ranking of propellers
    sortedPropNames = sorted(maxThrustList, key=maxThrustList.get, reverse=True)
    rankNumber = 1
    for name in sortedPropNames:
        rankRows.append(Label(root, 
                        text=f"{str(rankNumber)}. {name} Thrust: {str(maxThrustList[name])} {dropDownUnits} at {str(powerInWatts[name])} W",
                        font="Roboto 12", bg=colorSelection, wraplength=500, padx=40))
        rankRows[rankNumber-1].grid(row=6+rankNumber, column=1, columnspan=2, sticky='w')
        rankNumber+=1

def readFiles(filesToRead: list, maxThrust: dict, root, dropDownUnits: str, errorText: Label, colorSelection: str, maxIndices: list[int], rankRows: list[Label], dataFormat: str, powerLimitEntry: Entry)-> None:
    '''Read the spreadsheet, process the data, and display ranking of propellers'''
    powerInW = {} #stores corresponding power (in watts) at max thrust in order of props with descending thrust
    filesToPlot = {} #stores files to plot and its corresponding plot label
    sheetColNames = ['Thrust ('+dropDownUnits+')', 'Electrical Power (W)']
    maxThrust.clear() #clear list from last plot
    maxIndices.clear()
    filesToPlot.clear()

    # Get power limit from entry field
    powerLimitStr = powerLimitEntry.get().strip()
    powerLimit = None
    if powerLimitStr:
        try:
            powerLimit = float(powerLimitStr)
        except ValueError:
            errorText.config(text="ERROR: Power limit must be a valid number.")
            return

    # Determine column names based on data format
    if dataFormat == "LY-10KGF":
        sourceThrustCol = "Thrust-g"
        sourcePowerCol = "Electrical-P-P"
        headerRow = 11  # LY-10KGF format has header at row 11 (0-indexed)
    else:  # Tyto Series 1585
        sourceThrustCol = sheetColNames[0]
        sourcePowerCol = sheetColNames[1]
        headerRow = 0  # Standard header row

    try:
        for file in filesToRead:
            fileExtension = (file.split("."))[-1]
            fileName = file.split(".")[0]
            if(fileName not in filesToPlot):
                if fileExtension=="csv":
                    if dataFormat == "LY-10KGF":
                        # Read LY-10KGF format CSV file with header at row 11 (0-indexed)
                        try:
                            # Skip metadata rows (0-10) and read from row 11 with proper headers
                            currCsv = pd.read_csv(currDir+"/"+file, skiprows=11)
                            
                            # LY-10KGF CSV format uses column names: Thrust-g and Electrical-P-P
                            if "Thrust-g" not in currCsv.columns or "Electrical-P-P" not in currCsv.columns:
                                raise ValueError("CSV file must contain 'Thrust-g' and 'Electrical-P-P' columns for LY-10KGF format")
                            
                            # Extract thrust and power columns
                            thrust_col = "Thrust-g"
                            power_col = "Electrical-P-P"
                            
                            # Create a clean dataframe with only the columns we need
                            currCsv = currCsv[[thrust_col, power_col]].copy()
                            
                            # Verify data is numeric
                            currCsv[thrust_col] = pd.to_numeric(currCsv[thrust_col], errors='coerce')
                            currCsv[power_col] = pd.to_numeric(currCsv[power_col], errors='coerce')
                            
                            # Remove rows with NaN values
                            currCsv = currCsv.dropna(subset=[thrust_col, power_col])
                            
                            if len(currCsv) == 0:
                                raise ValueError("No valid numeric data found in CSV file")
                            
                            # Convert thrust from grams to selected units
                            if dropDownUnits == "lbf":
                                conversionFactor = 0.00220462  # grams to lbf
                            else:  # kg
                                conversionFactor = 0.001  # grams to kg
                            
                            # Convert thrust units and take absolute value
                            currCsv[thrust_col] = (currCsv[thrust_col] * conversionFactor).abs()
                            
                            # Rename columns to match expected format
                            currCsv.columns = sheetColNames
                            filesToPlot[fileName] = currCsv
                            
                            # Calculate original max index for plotting (always plot full dataset)
                            originalMaxIndex = currCsv[sheetColNames[0]].idxmax()
                            powerColIndex = currCsv.columns.get_loc(sheetColNames[1])
                            plotIndex = originalMaxIndex if originalMaxIndex<2 else originalMaxIndex-2
                            
                            if powerLimit is not None:
                                # Find thrust at power limit for ranking
                                thrustAtLimit, powerAtLimit, limitIndex = findThrustAtPowerLimit(currCsv, powerLimit, sheetColNames[1], sheetColNames[0])
                                if thrustAtLimit is not None:
                                    maxVal = thrustAtLimit
                                    powerAtMax = powerAtLimit
                                else:
                                    # No data before limit, use max thrust
                                    maxVal = max(currCsv[sheetColNames[0]])
                                    powerAtMax = currCsv.iloc[plotIndex, powerColIndex]
                            else:
                                maxVal = max(currCsv[sheetColNames[0]])
                                powerAtMax = currCsv.iloc[plotIndex, powerColIndex]

                            maxIndices.append(plotIndex)  # Use original max index for plotting
                            powerInW[fileName] = "%.1f" % powerAtMax #format power to one decimal place
                            maxThrust[fileName] = "%.3f" % maxVal #format thrust to three decimal places
                        except Exception as e:
                            continue
                    else:
                        # Tyto Series 1585 format CSV
                        try:
                            currCsv = pd.read_csv(currDir+"/"+file, usecols=sheetColNames)
                            
                            # Verify columns exist and data is numeric
                            currCsv[sheetColNames[0]] = pd.to_numeric(currCsv[sheetColNames[0]], errors='coerce')
                            currCsv[sheetColNames[1]] = pd.to_numeric(currCsv[sheetColNames[1]], errors='coerce')
                            
                            # Remove rows with NaN values
                            currCsv = currCsv.dropna(subset=sheetColNames)
                            
                            if len(currCsv) == 0:
                                raise ValueError("No valid numeric data found in CSV file")
                            
                            currCsv[sheetColNames[0]] = currCsv[sheetColNames[0]].abs() #take absolute value in case user didn't check the box to make thrust positive
                            filesToPlot[fileName] = currCsv

                            # Calculate original max index for plotting (always plot full dataset)
                            originalMaxIndex = currCsv[sheetColNames[0]].idxmax()
                            powerColIndex = currCsv.columns.get_loc(sheetColNames[1])
                            plotIndex = originalMaxIndex if originalMaxIndex<2 else originalMaxIndex-2 #to avoid the wattage being artificially low when max thrust is at the time the throttle is cut
                            
                            if powerLimit is not None:
                                # Find thrust at power limit for ranking
                                thrustAtLimit, powerAtLimit, limitIndex = findThrustAtPowerLimit(currCsv, powerLimit, sheetColNames[1], sheetColNames[0])
                                if thrustAtLimit is not None:
                                    maxVal = thrustAtLimit
                                    powerAtMax = powerAtLimit
                                else:
                                    # No data before limit, use max thrust
                                    maxVal = max(currCsv[sheetColNames[0]])
                                    powerAtMax = currCsv.iloc[plotIndex, powerColIndex]
                            else:
                                maxVal = max(currCsv[sheetColNames[0]])
                                powerAtMax = currCsv.iloc[plotIndex, powerColIndex]

                            maxIndices.append(plotIndex)  # Use original max index for plotting
                            powerInW[fileName] = "%.1f" % powerAtMax #format power to one decimal place
                            maxThrust[fileName] = "%.3f" % maxVal #format thrust to three decimal places
                        except Exception as e:
                            continue
                elif fileExtension=="xlsx":
                    if dataFormat == "LY-10KGF":
                        # Read LY-10KGF format with header at row 11
                        currXl = pd.read_excel(currDir+"/"+file, header=headerRow, usecols=[sourceThrustCol, sourcePowerCol])
                        try:
                            # Convert thrust from grams to selected units
                            # 1 gram = 0.00220462 lbf or 0.001 kg
                            if dropDownUnits == "lbf":
                                conversionFactor = 0.00220462  # grams to lbf
                            else:  # kg
                                conversionFactor = 0.001  # grams to kg
                            
                            # Convert thrust units
                            currXl[sourceThrustCol] = currXl[sourceThrustCol] * conversionFactor
                            
                            # Rename columns to match expected format
                            currXl = currXl.rename(columns={sourceThrustCol: sheetColNames[0], sourcePowerCol: sheetColNames[1]})
                            currXl[sheetColNames[0]] = currXl[sheetColNames[0]].abs()  #take absolute value
                            filesToPlot[fileName] = currXl
                            
                            # Calculate original max index for plotting (always plot full dataset)
                            originalMaxIndex = currXl[sheetColNames[0]].idxmax()
                            powerColIndex = currXl.columns.get_loc(sheetColNames[1])
                            plotIndex = originalMaxIndex if originalMaxIndex<2 else originalMaxIndex-2 #to avoid the wattage being artificially low when max thrust is at the time the throttle is cut
                            
                            if powerLimit is not None:
                                # Find thrust at power limit for ranking
                                thrustAtLimit, powerAtLimit, limitIndex = findThrustAtPowerLimit(currXl, powerLimit, sheetColNames[1], sheetColNames[0])
                                if thrustAtLimit is not None:
                                    maxVal = thrustAtLimit
                                    powerAtMax = powerAtLimit
                                else:
                                    # No data before limit, use max thrust
                                    maxVal = max(currXl[(sheetColNames[0])])
                                    powerAtMax = currXl.iloc[plotIndex, powerColIndex]
                            else:
                                maxVal = max(currXl[(sheetColNames[0])])
                                powerAtMax = currXl.iloc[plotIndex, powerColIndex]

                            maxIndices.append(plotIndex)  # Use original max index for plotting
                            powerInW[fileName] = "%.1f" % powerAtMax #format power to one decimal place
                            maxThrust[fileName] = "%.3f" % maxVal #format thrust to three decimal places
                        except Exception as e:
                            continue
                    else:
                        # Tyto Series 1585 format (original)
                        currXl = pd.read_excel(currDir+"/"+file, usecols=sheetColNames)
                        try:
                            currXl[sheetColNames[0]] = currXl[sheetColNames[0]].abs()  #take absolute value in case user didn't check the box to make thrust positive
                            filesToPlot[fileName] = currXl
                            
                            # Calculate original max index for plotting (always plot full dataset)
                            originalMaxIndex = currXl[sheetColNames[0]].idxmax()
                            powerColIndex = currXl.columns.get_loc(sheetColNames[1])
                            plotIndex = originalMaxIndex if originalMaxIndex<2 else originalMaxIndex-2 #to avoid the wattage being artificially low when max thrust is at the time the throttle is cut
                            
                            if powerLimit is not None:
                                # Find thrust at power limit for ranking
                                thrustAtLimit, powerAtLimit, limitIndex = findThrustAtPowerLimit(currXl, powerLimit, sheetColNames[1], sheetColNames[0])
                                if thrustAtLimit is not None:
                                    maxVal = thrustAtLimit
                                    powerAtMax = powerAtLimit
                                else:
                                    # No data before limit, use max thrust
                                    maxVal = max(currXl[(sheetColNames[0])])
                                    powerAtMax = currXl.iloc[plotIndex, powerColIndex]
                            else:
                                maxVal = max(currXl[(sheetColNames[0])])
                                powerAtMax = currXl.iloc[plotIndex, powerColIndex]

                            maxIndices.append(plotIndex)  # Use original max index for plotting
                            powerInW[fileName] = "%.1f" % powerAtMax #format power to one decimal place
                            maxThrust[fileName] = "%.3f" % maxVal #format thrust to three decimal places
                        except:
                            continue
                else:
                    print("Error: Something went wrong. All files must be xlsx or csv.")
                    exit(2)

        errorText.config(text="")
        clearRanking(rankRows)
        displayRanking(root, maxThrust, rankRows, colorSelection, dropDownUnits, powerInW, powerLimit)

        #Call graphing function
        generatePlot(filesToPlot, dropDownUnits, sheetColNames, maxIndices, powerLimit)
    except:
        errorText.config(text=f"Error: No column found for thrust with the following units: {dropDownUnits}\nCheck that you selected the correct units."+
                         f"\nThe xlsx or csv file should be the exact formatting as outputted by the {dataFormat} thrust stand.")
        #clear output from previous run
        clearRanking(rankRows)
        plt.close()

def generatePlot(filesArray: dict, units: str, sheetNames: list[str], maxIndices: list[int], powerLimit: float = None) -> None:
    '''Produces a plot of thrust vs power from pandas DataFrame object'''
    thrust = sheetNames[0]
    power = sheetNames[1]

    patchesArr = []
    index=0

    plt.clf()
    for spreadsheet in filesArray.values():
        # Plot all data if power limit is specified, otherwise use maxIndices for truncation
        if powerLimit is not None:
            x = spreadsheet[power]
            y = spreadsheet[thrust]
        else:
            x = (spreadsheet[power])[:maxIndices[index]]
            y = (spreadsheet[thrust])[:maxIndices[index]]
        myPlot = plt.plot(x, y, linewidth=.5)
        currColor = myPlot[0].get_color()
        plt.xlabel("Power (W)")
        plt.ylabel("Thrust ("+units+")")
        patchesArr.append(patch.Patch(color=currColor, label=list(filesArray.keys())[index]))
        index+=1
    
    # Draw vertical dotted line at power limit if provided
    if powerLimit is not None:
        plt.axvline(x=powerLimit, color='red', linestyle='--', linewidth=1.5)
        patchesArr.append(patch.Patch(color='red', linestyle='--', label=f'Power Limit: {powerLimit} W'))
    
    # Set y-axis to start at 0
    plt.ylim(bottom=0)
    
    # Enable minor ticks and gridlines
    plt.minorticks_on()
    plt.grid(True, which='major')
    plt.grid(True, which='minor', alpha=0.3, linestyle=':')
    plt.legend(loc="lower right", handles=patchesArr)
    plt.show()

def isPlotEmpty(plot) -> bool:
    '''This function returns true if the Matplotlib plot is empty, and false otherwise.'''
    return len(plot.axes) == 0