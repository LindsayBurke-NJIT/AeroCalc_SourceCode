from tkinter import *

def initEmpty(tabControl, tab1: Frame, fontName: str, colorSelection: str):
    emptyText = Label(tab1, text="", font=fontName, bg=colorSelection)
    emptyText.grid(row=0, column=0, sticky='nsew')