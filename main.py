from PIL import Image 
from pytesseract import pytesseract
import cv2 
import threading
import pywhatkit as kt
from reportlab.pdfgen.canvas import Canvas
import base64
import os
import json


#tesseract_path = r"C:\Program Files\Tesseract-OCR/tesseract.exe"
def json_func() :

    with open('app.json') as user_file:
        file_contents = user_file.read()

    file_contents=file_contents.replace('{"tesseract_path": "','' )
    file_contents=file_contents.replace('"}','' )
    file_contents=file_contents.replace('"','' )

    if os.path.exists(file_contents) is True:
        return file_contents
    else:
        print("_____TESSERACT SETUP_____")
        print("ENTER THE TESSERACT PATH TO CONTINUE.")
        tesseract_path=str(input())
        with open('app.json', 'r') as f:
            json_data = json.load(f)
        json_data['tesseract_path'] = tesseract_path

        with open('app.json', 'w') as f:
            f.write(json.dumps(json_data))
    



def img_reader(imgpath, tesseract_path):
    img = Image.open(imgpath)
    pytesseract.tesseract_cmd = tesseract_path 
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
                stat=img_reader(command,json_func())
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

                    if command=='Q' or command=='new':
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


    elif zero=='info':
        print("For extracting text from image: \n extract text -img <address>" )
        print("For encoding image : \n img -encode <address>")
        print("To search the extracted text : \n text -search")
        print("To save the extracted text as pdf or txt : \n text -save as <address>")
        print("To share the extracted text : \n text -share")

    else:
            pass

    

if __name__=='__main__':
    json_func()
    print("WELCOME TO IMG EXTRACTOR : ")
    while True:
        main()
