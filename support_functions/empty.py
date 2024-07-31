from tkinter import *

def initEmpty(tabControl, tab1: Frame, fontName: str, colorSelection: str):
    tabControl.add(tab1, text="Empty", state=NORMAL)
    tabControl.grid(row=0, column=2, sticky='nsew')
    emptyText = Label(tab1, text="", font=fontName, bg=colorSelection)
    emptyText.grid(row=1, column=2, sticky='nsew', padx=(0,600))