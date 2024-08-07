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

    errorText = Label(tab1, text="", font=fontName, bg=colorSelection, fg="red", wraplength=450)
    errorText.grid(column=1, row=2, columnspan=5)

    fileSelectText = Label(tab1, text="Select a Folder:", font=fontName+' 15 bold', bg=colorSelection, fg=buttonTextColor)
    fileSelectText.grid(column=1, row=0, columnspan=1, padx=10, pady=10, sticky='w')

    filesToRead = [] #list of spreadsheet files in the directory that can be plotted
    maxThrust = {} #dictionary of max thrusts {fileName : maxThrust}
    maxIndices = []
    rankRows = [] #stores filenames in order of descending thrust

    fileSelectButton = Button(tab1, text="Select Folder", wraplength=400, width=40, justify=LEFT, bg=buttonColor, fg=buttonTextColor, command=lambda: selectFolder(errorText, fileSelectButton, filesToRead))
    fileSelectButton.grid(column=2, row=0, columnspan=1, padx=10, pady=10, sticky='w')

    #Creates thrust unit dropdown menu
    options = ["lbf", "kg"]
    clicked = StringVar()
    clicked.set("lbf")
    dropText = Label(tab1, text="Thrust Units:", bg=colorSelection,font=fontName+' 15 bold')
    dropText.grid(row=1, column=1, pady=10, columnspan=1, sticky='w', padx=10)
    unitDropDown = OptionMenu(tab1, clicked, *options)
    unitDropDown.config(highlightthickness=1, bg=buttonColor, fg=buttonTextColor)
    unitDropDown.grid(row=1, column=2, columnspan=1, sticky='w', padx=10)

    startPlotButton = Button(tab1, text="Plot", width=40, bg=buttonColor, fg=buttonTextColor, command=lambda: readFiles(filesToRead, maxThrust, tab1, clicked.get(), errorText, colorSelection, maxIndices, rankRows))
    startPlotButton.grid(row=3, column=1, columnspan=2, pady=10, padx=(100, 0), sticky='w')

    downloadPlotsButton = Button(tab1, text="Download", bg="black", fg="white", width=10, height=1, wraplength=100, command=lambda: downloadPlot(errorText))
    downloadPlotsButton.grid(row=3, column=2, padx=(250, 40), sticky='w')

    rankingTextLabel = Label(tab1, text="Propeller Ranking:", font=fontName+" 15 bold", bg=colorSelection)
    rankingTextLabel.grid(row=4, column=1, columnspan=2, sticky='nsw', pady=20, padx=150)

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

def readFiles(filesToRead: list, maxThrust: dict, root, dropDownUnits: str, errorText: Label, colorSelection: str, maxIndices: list[int], rankRows: list[Label])-> None:
    '''Read the spreadsheet, process the data, and display ranking of propellers'''
    powerInW = {} #stores corresponding power (in watts) at max thrust in order of props with descending thrust
    filesToPlot = {} #stores files to plot and its corresponding plot label
    sheetColNames = ['Thrust ('+dropDownUnits+')', 'Electrical Power (W)']
    maxThrust.clear() #clear list from last plot
    maxIndices.clear()

    try:
        for file in filesToRead:
            fileExtension = (file.split("."))[-1]
            fileName = file.split(".")[0]
            if fileExtension=="csv":
                currCsv = pd.read_csv(currDir+"/"+file, usecols=sheetColNames)
                try:
                    currCsv[sheetColNames[0]] = currCsv[sheetColNames[0]].abs() #take absolute value in case user didn't check the box to make thrust positive
                    filesToPlot[fileName] = currCsv

                    maxVal = max(currCsv[sheetColNames[0]])
                    maxIndex = currCsv[sheetColNames[0]].idxmax()
                    powerColIndex = currCsv.columns.get_loc(sheetColNames[1])
                    maxIndex = maxIndex if maxIndex<2 else maxIndex-2 #to avoid the wattage being artificially low when max thrust is at the time the throttle is cut
                    maxIndices.append(maxIndex)
                    powerAtMax = currCsv.iloc[maxIndex, powerColIndex]

                    powerInW[fileName] = "%.1f" % powerAtMax #format power to one decimal place
                    maxThrust[fileName] = "%.3f" % maxVal #format thrust to three decimal places
                except:
                    continue
            elif fileExtension=="xlsx":
                currXl = pd.read_excel(currDir+"/"+file, usecols=sheetColNames)
                try:
                    currXl[sheetColNames[0]] = currXl[sheetColNames[0]].abs()  #take absolute value in case user didn't check the box to make thrust positive
                    filesToPlot[fileName] = currXl
                    
                    maxVal = max(currXl[(sheetColNames[0])])
                    maxIndex = currXl[sheetColNames[0]].idxmax()
                    powerColIndex = currXl.columns.get_loc(sheetColNames[1])
                    maxIndex = maxIndex if maxIndex<2 else maxIndex-2 #to avoid the wattage being artificially low when max thrust is at the time the throttle is cut
                    maxIndices.append(maxIndex)
                    powerAtMax = currXl.iloc[maxIndex, powerColIndex]

                    powerInW[fileName] = "%.1f" % powerAtMax #format power to one decimal place
                    maxThrust[fileName] = "%.3f" % maxVal #format thrust to three decimal places
                except:
                    continue
            else:
                print("Error: Something went wrong. All files must be xlsx or csv.")
                exit(2)

        errorText.config(text="")
        clearRanking(rankRows)

        #Display ranking of propellers
        sortedPropNames = sorted(maxThrust, key=maxThrust.get, reverse=True)
        rankNumber = 1
        for name in sortedPropNames:
            rankRows.append(Label(root, 
                            text=f"{str(rankNumber)}. {name} Max Thrust: {str(maxThrust[name])} {dropDownUnits} at {str(powerInW[name])} W",
                            font="Roboto 12", bg=colorSelection, wraplength=500, padx=40))
            rankRows[rankNumber-1].grid(row=4+rankNumber, column=1, columnspan=2, sticky='w')
            rankNumber+=1

        #Call graphing function
        generatePlot(filesToPlot, dropDownUnits, sheetColNames, maxIndices)
    except:
        errorText.config(text=f"Error: No column found for thrust with the following units: {dropDownUnits}\nCheck that you selected the correct units."+
                         "\nThe xlsx or csv file should be the exact formatting as outputted by the Series 1585 thrust stand.")
        #clear output from previous run
        clearRanking(rankRows)

def generatePlot(filesArray: dict, units: str, sheetNames: list[str], maxIndices: list[int]) -> None:
    '''Produces a plot of thrust vs power from pandas DataFrame object'''
    thrust = sheetNames[0]
    power = sheetNames[1]

    patchesArr = []
    index=0
    for spreadsheet in filesArray.values():
        x = (spreadsheet[power])[:maxIndices[index]]
        y = (spreadsheet[thrust])[:maxIndices[index]]
        myPlot = plt.plot(x, y, linewidth=.5)
        currColor = myPlot[0].get_color()
        plt.xlabel("Power (W)")
        plt.ylabel("Thrust ("+units+")")
        patchesArr.append(patch.Patch(color=currColor, label=list(filesArray.keys())[index]))
        index+=1
    plt.grid()
    plt.legend(loc="lower right", handles=patchesArr)

def downloadPlot(errorLabel: Label) -> None:
    '''Downloads the generated plot to the user's device'''
    fileName = filedialog.asksaveasfilename(confirmoverwrite=True, initialfile="untitled.png", defaultextension="png", filetypes=[(".png", ".png")])
    if(fileName!=""):
        plt.savefig(fileName)

def isPlotEmpty(plot) -> bool:
    '''This function returns true if the Matplotlib plot is empty, and false otherwise.'''
    return len(plot.axes) == 0