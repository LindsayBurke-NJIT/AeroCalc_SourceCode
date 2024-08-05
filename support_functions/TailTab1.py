class TailTab1:
    def __init__(self):
        self.wingArea = 0
        self.chord = 0
        self.tailArea = 0
        self.myLength = 0
        self.vTailArea = 0
        self.vLength = 0
        self.wingSpan = 0

    #setters
    def setWingArea(self, newArea: float) -> None:
        self.wingArea = newArea
    def setChord(self, newChord: float) -> None:
        self.chord = newChord
    def setTailArea(self, newTA: float) -> None:
        self.tailArea = newTA
    def setLength(self, newL: float) -> None:
        self.myLength = newL
    def setVerticalTailArea(self, newVTA: float) -> None:
        self.vTailArea = newVTA
    def setVerticalLength(self, newVL: float) -> None:
        self.vLength = newVL
    def setWingSpan(self, newWS: float) -> None:
        self.wingSpan = newWS