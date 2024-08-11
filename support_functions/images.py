import os, pathlib

def addImg(fileName: str) -> (str | bool):
    try:
        currentDir = pathlib.Path(__file__).parent.resolve()
        imgPath = os.path.join(currentDir, f"..\\images\\{fileName}")
        return imgPath
    except:
        return False