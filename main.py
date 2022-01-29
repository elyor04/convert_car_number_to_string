from cv2 import (
    VideoCapture, rectangle, putText, imshow,
    FONT_HERSHEY_TRIPLEX, waitKey, destroyAllWindows)
from car_num_to_str import (
    sozQiymat, sozlash, CarNumToStr)

__nmrlar = list()
def yigibTekshir(text: str) -> str:
    if text != '?': __nmrlar.append(text)
    nmr_ln, aniq = len(__nmrlar), '?'

    if nmr_ln >= 4:
        for i in __nmrlar:
            foiz = (__nmrlar.count(i) / nmr_ln) * 100
            if foiz > 60:

                if '6' in i[2:6]:
                    if text[2].isalpha():
                        a = [
                            i[:3] +'0'+ i[4:], i[:4] +'0'+ i[5:], i[:5] +'0'+ i[6:],
                            i[:3] +"00"+ i[5:], i[:4] +"00"+ i[6:], i[:3] +"000"+ i[6:]]
                    else:
                        a = [
                            i[:2] +'0'+ i[3:], i[:3] +'0'+ i[4:], i[:4] +'0'+ i[5:],
                            i[:2] +"00"+ i[4:], i[:3] +"00"+ i[5:], i[:2] +"000"+ i[5:]]
                    
                    for j in a:
                        foiz = (__nmrlar.count(j) / nmr_ln) * 100
                        if (j[2:6] != i[2:6]) and (foiz > 30):
                            aniq = j
                            break
                    else: aniq = i
                else: aniq = i
                __nmrlar.clear()
                break
    
    if len(__nmrlar) == 8:
        __nmrlar.clear()
    return aniq


kam = VideoCapture(0)
oby = CarNumToStr(debug=True)
eni, buyi = sozQiymat(kam.read()[1], yuza=500000)
eni += 4

while True:
    img = sozlash(kam.read()[1], eni, buyi)
    oby.start(img)
    texts, cords = oby.getTexts(), oby.getCordinates()

    for text, [(x,y), (x2,y2)] in zip(texts, cords):
        aniq = yigibTekshir(text)
        if aniq != '?': print(f"aniq: {aniq}")
        rectangle(img, (x,y), (x2,y2), (50,250,50), 2)
        putText(img, text, (x,y2+30), FONT_HERSHEY_TRIPLEX, 1.0, (5,250,5), 1)
    imshow("nomer", img)

    if waitKey(4) & 0xFF==ord('q'):
        break
kam.release()
destroyAllWindows()
