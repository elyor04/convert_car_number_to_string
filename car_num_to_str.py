from cv2 import (
    imshow, cvtColor, resize, CascadeClassifier, adaptiveThreshold, COLOR_BGR2GRAY, INTER_AREA,
    INTER_LINEAR, INTER_CUBIC, bitwise_not, ADAPTIVE_THRESH_MEAN_C, THRESH_BINARY_INV)
from skimage.segmentation._clear_border import clear_border
from pytesseract import image_to_string
from math import sqrt
from pandas.io.api import read_sql
from numpy import ndarray

def sozQiymat(img:ndarray=None, eni:int=None, buyi:int=None, yuza:int=100000) -> tuple[int,int]:
    if (eni is None) or (buyi is None):
        buyi, eni = img.shape[:2]
    k = round(sqrt(yuza / (eni * buyi)), 4)
    x, y = int(eni * k), int(buyi * k)
    return (x, y)

def sozlash(img:ndarray, eni:int=None, buyi:int=None, sifat:bool=False, auto:bool=False, yuza:int=100000) -> ndarray:
    if auto: x, y = sozQiymat(img, yuza=yuza)
    else: x, y = eni, buyi
    buyi, eni = img.shape[:2]

    if (x <= eni) and (y <= buyi):
        return resize(img, (x, y), interpolation=INTER_AREA)
    elif (x >= eni) and (y >= buyi):
        if sifat:
            return resize(img, (x, y), interpolation=INTER_CUBIC)
        else:
            return resize(img, (x, y), interpolation=INTER_LINEAR)
    else:
        return resize(img, (x, y))

__tkshr = [
	"01", "10", "20", "25", "30", "40", "50",
	"60", "70", "75", "80", "85", "90", "95"]

def cleanNumber(text: str) -> str:
    text = ''.join([i if ord(i) < 128 else '' for i in text]).strip()
    if ' ' in text: text = text.replace(' ', '')
    if 'I' in text: text = text.replace('I', '')
    tx_ln, rtrn = len(text), '?'

    if tx_ln == 8:
        if text[1] == '1': text = "01" + text[2:]
        elif text[1] != '5': text = text[0] +'0'+ text[2:]

        if (text[:2] in __tkshr) and text[tx_ln-2:].isalpha():
            for i in "GUO":
                if i in text[3:5]:
                    text = text[:3] + text[3:5].replace(i, '0') + text[5:]
            
            if text[2].isalpha() and (text[2] not in "GUO"):
                if text[5] in "GUO": text = text[:5] +'0'+ text[6:]
                if text[3:6].isdigit(): rtrn = text
            
            elif text[5].isalpha() and (text[5] not in "GUO"):
                if text[2] in "GUO": text = text[:2] +'0'+ text[3:]
                if text[2:5].isdigit(): rtrn = text
            
            elif (text[2].isalpha() and text[3:6].isdigit()) or (text[5].isalpha() and text[2:5].isdigit()):
                rtrn = text
    return rtrn

class CarNumToStr(object):
    def __init__(self, aniqlik:bool=True, debug:bool=False) -> None:
        super(CarNumToStr, self).__init__()
        self.__text, self.__cord = list(), list()
        self.__aniq, self.__debug = aniqlik, debug
        self.__cascade = CascadeClassifier("haarcascade_russian_plate_number.xml")
    
    def __moshinaRaqami(self, img:ndarray) -> list:
        crp_list = list()
        plates = self.__cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=4)
        for (x,y,w,h) in plates:
            if w*h >= 8000:
                x2, y2 = x+w, y+h
                crp_list.append(img[y:y2, x:x2])
                self.__cord.append([(x,y), (x2,y2)])
        return crp_list
    
    def __img2str(self, crp_img:ndarray) -> str:
        img = adaptiveThreshold(
            crp_img, 255, ADAPTIVE_THRESH_MEAN_C, THRESH_BINARY_INV, 23, 8)
        img = bitwise_not(clear_border(img))
        if self.__debug: imshow("oq_qora", img)
        text = image_to_string(
            img, lang="eng", config="-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 7")
        if self.__aniq:
            return cleanNumber(text)
        else:
            return ''.join([i if ord(i) < 128 else '' for i in text]).strip()
	
    def start(self, img:ndarray) -> None:
        self.__text, self.__cord = list(), list()
        if img.ndim == 3:
            img = cvtColor(img, COLOR_BGR2GRAY)
        crp_imgs = self.__moshinaRaqami(img)
        for crp_img in crp_imgs:
            crp_img = sozlash(crp_img, auto=True, yuza=20000)
            self.__text.append(self.__img2str(crp_img))
    
    def getTexts(self) -> list:
        return self.__text
    def getCordinates(self) -> list:
        return self.__cord

def sqlToExcel(sql_connection, sql_selection:str, name_for_file:str) -> None:
    data = read_sql(sql_selection, sql_connection)
    data.to_excel(name_for_file)
