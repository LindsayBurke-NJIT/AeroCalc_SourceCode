import os, pathlib
def addImg(fileName: str) -> (str | bool):
    try:
        currentDir = pathlib.Path(__file__).parent.resolve() # current directory
        imgPath = os.path.join(currentDir, "..\\images\\"+fileName)
        return imgPath
    except:
        return False