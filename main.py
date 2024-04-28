from PIL import Image 
from pytesseract import pytesseract
import cv2 
import threading
import pywhatkit as kt
from reportlab.pdfgen.canvas import Canvas
import base64


path_to_tesseract = r"C:\Program Files\Tesseract-OCR/tesseract.exe"

def img_reader(imgpath):
    img = Image.open(imgpath)
    pytesseract.tesseract_cmd = path_to_tesseract 
    text = pytesseract.image_to_string(img) 
    print(text)

def qr_reader(img_path):
    img = cv2.imread(img_path)
    detector = cv2.QRCodeDetector()
    data, bbox = detector.detectAndDecode(img)

    if bbox is not None:
        return data
    else:
        return None


def content(image_path:str):    
    if qr_reader(image_path) is not None:
        return qr_reader(image_path)
    else:
        return img_reader(image_path)

def save(data:str , com:str) -> None:
    if 'pdf' in com:
        command=com.replace("text -save as ",'')
        canvas = Canvas(command)
        canvas.drawString(0, 0, data)
        return None
    
    elif 'txt' in com:
        command=com.replace("text -save as ",'')
        with open(command, 'w') as f:
            f.write(data)
        return None


def main() -> None:
    
    zero=str(input())
    if zero=='start' or zero=='Start':
        command=str(input())

        if 'extract text -img ' in command:

            command=command.replace('extract text -img ','')
            img = cv2.imread(command)
            detector = cv2.QRCodeDetector()
            data, bbox , straight_qrcode= detector.detectAndDecode(img)

            if bbox is not None:
                stat=data
            else:
                stat=img_reader(command)
            print(stat)

            print("CHOOSE AN OPERATION TO PERFORM WITH THIS TEXT.[enter Q to exit]")
            while True:
                    command=str(input())

                    if 'text -search' in command:
                        kt.search(stat)
                        continue

                    if 'text -save' in command:
                        save(stat,command)
                        print('file saved')
                    
                    if 'text -share' in command:
                        num=str(input('enter number :'))
                        kt.sendwhatmsg(num, stat)
                    if command=='Q':
                        break
                    
                    if command=='new':
                        main()

        elif 'img -encode' in command:

                with open(command.replace('img -encode ', ''), "rb") as image2string: 
                    converted_string = base64.b64encode(image2string.read()) 
                print(converted_string)

                while True:

                    command=str(input())
                    if 'text -save' in command:
                        save(stat,command)
                        print('file saved')
                    if command=='new':
                        main()
                    else:
                        pass
        else:
                pass
        
    else:
            pass

    

if __name__=='__main__':
    print("WELCOME TO IMG EXTRACTOR : ")
    while True:
        main()
