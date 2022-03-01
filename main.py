from cv2 import (
    VideoCapture, rectangle, putText, imshow,
    FONT_HERSHEY_TRIPLEX, waitKey, destroyAllWindows)
from car_num_to_str import (
    CarNumToStr, yigibTekshir, sozQiymat, sozlash)

oby = CarNumToStr(debug=True)
kam = VideoCapture(0)
waitKey(1000)
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
