from tkinter import *
import support_functions.images as images

def constructTab(tabControl, tab1: Frame, colorSelection: str) -> None:
    global aeroLogo #declared PhotoImage global to avoid garbage collection

    tabControl.add(tab1, text="Home", state=NORMAL)
    tabControl.grid(column=1, row=0, sticky='nsew')
    homeTitle = Label(tab1, text="Flylanders™ AeroCalc", bg=colorSelection, font="Roboto 20 bold")
    homeTitle.grid(row=0, column=0, columnspan=10, sticky='nsew', padx=120)

    welcomeText = Label(tab1, wraplength=400, font="Roboto 14", bg=colorSelection, text="Welcome to AeroCalc, created by and for the NJIT Flylanders™ SAE Aero Design Team.")
    welcomeText.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=75, pady=(50, 0))
    
    aeroImg = "aeroLogo.png"
    imgPath = None
    try:
        imgPath = images.addImg(aeroImg)
        aeroLogo = PhotoImage(file=imgPath)
        aeroPhoto = Label(tab1, image = aeroLogo, width=200, height=200, bg=colorSelection)
        aeroPhoto.grid(row=2, column=0, columnspan=2, sticky='nsew', padx = 150, pady=20)
    except:
        print(f"{aeroImg} not found at {imgPath}")

    descrText = Label(tab1, wraplength=400, font="Roboto 14", bg=colorSelection, text="This program is a compilation of calculators and tools used by each of our subteams to design our competition RC plane.")
    descrText.grid(row=3, column=0, columnspan=2, sticky='nsew')

    creditText = Label(tab1, wraplength=200, font="Roboto 10", bg=colorSelection, text="Created By: Lindsay Burke")
    creditText.grid(row=4, column=0, sticky='sw', pady=(100, 0), padx=(10, 0))

    versionText = Label(tab1, font="Roboto 10", bg=colorSelection, text="v1.0.0")
    versionText.grid(row=4, column=1, sticky='se', padx=(0, 10), pady=(100,0))