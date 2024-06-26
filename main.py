from PIL import Image 
from pytesseract import pytesseract
import cv2 
import threading
import pywhatkit as pwk
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate as sdt
from reportlab.lib.units import cm
import base64
import os
import json
from datetime import datetime
import pyttsx3 as pt


engine = pt.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()



#tesseract_path = r"C:\Program Files\Tesseract-OCR/tesseract.exe"
def jfunc() :

    with open('app.json') as jsonfile:
        adres = jsonfile.read()

    adres=adres.replace('{"tesseract_path": "','' )
    adres=adres.replace('"}','' )
    adres=adres.replace('"','' )

    if os.path.exists(adres) is True:
        return adres
    else:
        print("_____TESSERACT SETUP_____")
        print("ENTER THE TESSERACT PATH TO CONTINUE.")
        tesseract_path=str(input())
        with open('app.json', 'r') as f:
            jsondata = json.load(f)
        jsondata['tesseract_path'] = tesseract_path

        with open('app.json', 'w') as f:
            f.write(json.dumps(jsondata))
    
def sjson():
    
        with open('speak.json') as jsonfile:
            adres = jsonfile.read()

        adres=adres.replace('{"speak": "','' )
        adres=adres.replace('"}','' )
        adres=adres.replace('"','' )

        if adres=="true":
            with open('speak.json', 'r') as f:
                jsondata = json.load(f)
            jsondata['speak'] = "false"

            with open('speak.json', 'w') as f:
                f.write(json.dumps(jsondata))
        else:
            with open('speak.json', 'r') as f:
                jsondata = json.load(f)
            jsondata['speak'] = "true"

            with open('speak.json', 'w') as f:
                f.write(json.dumps(jsondata))
        print("Speak properties changed.")

def img_reader(imgpath, tesseract_path):
    img = Image.open(imgpath)
    pytesseract.tesseract_cmd = tesseract_path 
    text = pytesseract.image_to_string(img) 
    return text

def qr_reader(img_path):
    img = cv2.imread(img_path)
    detector = cv2.QRCodeDetector()
    data, bbox = detector.detectAndDecode(img)

    if bbox is not None:
        return data
    else:
        return None

def save(text:str , com:str) -> None:
    if 'pdf' in com:
        command=com.replace("text -save as ",'')
        fl = sdt(command,pagesize=A4,rightMargin=2*cm,leftMargin=2*cm,topMargin=2*cm,bottomMargin=2*cm)
        fl.build([Paragraph(text),])
        return None
    
    elif 'txt' in com:
        command=com.replace("text -save as ",'')
        with open(command, 'w') as f:
            f.write(text)
        return None


def main() -> None:
    print("TO START NEW INSTANCE ENTER NEW OR 'Q")
    zero=str(input())
    if zero=='start' or zero=='Start':
        command=str(input(">>>>"))

        if 'extract text -img ' in command:

            command=command.replace('extract text -img ','')
            img = cv2.imread(command)
            detector = cv2.QRCodeDetector()
            data, bbox , straight_qrcode= detector.detectAndDecode(img)

            if bbox is not None:
                stat=data
            else:
                stat=img_reader(command,jfunc())
            print(stat)

            print("CHOOSE AN OPERATION TO PERFORM WITH THIS TEXT.[enter Q to exit]")
            while True:
                    command=str(input(">>>>"))

                    if 'text -search' in command:
                        pwk.search(stat)
                        print("Searching....")
                        continue

                    if 'text -save' in command:
                        save(stat,command)
                        print('file saved')
                        continue
                    
                    if 'text -share' in command:
                        num=str(input('enter number :'))
                        t= datetime.now()
                        print("do not close the window before confirmation message.")
                        if t.second<=35:
                            pwk.sendwhatmsg(num, stat,t.hour,t.minute+2)
                        else:
                            pwk.sendwhatmsg(num, stat,t.hour,t.minute+1)
                        print("Message Sent !!!")
                        continue

                    if command=='Q' or command=='new':
                        print("Instance ended, type \"start\" to continue")
                        main()

        elif 'img -encode' in command:

                with open(command.replace('img -encode ', ''), "rb") as image2string: 
                    stat = base64.b64encode(image2string.read()) 
                print(stat)
                print("CHOOSE AN OPERATION TO PERFORM WITH THIS TEXT.[enter Q to exit]")

                while True:
                    command=str(input(">>>>"))
                    if 'text -save' in command:
                        save(str(stat),command)
                        print("file saved !!")
                        
                    if command=='new' or command=='Q':
                        print("Instance ended, type \"start\" to continue")
                        main()
                    else:
                        pass
        
        else:
            pass

    elif zero=='speak':
        sjson()
        print("restart the program to see changes")
        raise DeprecationWarning
    elif zero=='info':
        print("For extracting text from image: \n extract text -img <address>" )
        print("For encoding image : \n img -encode <address>")
        print("To search the extracted text : \n text -search")
        print("To save the extracted text as pdf or txt : \n text -save as <address>")
        print("To share the extracted text : \n text -share")
        print("To encode the image : \n img-encode")
        print("To start new instance : \n Q or new")

    else:
            pass

def mainwithspeak() -> None:
    print("TO START NEW INSTANCE ENTER NEW OR 'Q")
    zero=str(input(">>>>"))
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
                stat=img_reader(command,jfunc())
            print(stat)
            speak(stat)

            print("CHOOSE AN OPERATION TO PERFORM WITH THIS TEXT.[enter Q to exit]")
            while True:
                    command=str(input(">>>>"))

                    if 'text -search' in command:
                        pwk.search(stat)
                        speak("Opening web")
                        continue

                    if 'text -save' in command:
                        save(stat,command)
                        speak('file saved')
                        continue
                    
                    if 'text -share' in command:
                        num=str(input('enter number :'))
                        t= datetime.now()
                        speak("do not close the window before confirmation message.")
                        if t.second<=35:
                            pwk.sendwhatmsg(num, stat,t.hour,t.minute+2)
                        else:
                            pwk.sendwhatmsg(num, stat,t.hour,t.minute+1)
                        speak("Message Sent !!!")
                        continue

                    if command=='Q' or command=='new':
                        speak("Instance ended, type \"start\" to continue")
                        main()

        elif 'img -encode' in command:

                with open(command.replace('img -encode ', ''), "rb") as image2string: 
                    stat = base64.b64encode(image2string.read()) 
                print(stat)
                print("CHOOSE AN OPERATION TO PERFORM WITH THIS TEXT.[enter Q to exit]")

                while True:
                    command=str(input(">>>>"))
                    if 'text -save' in command:
                        save(str(stat),command)
                        speak("file saved !!")
                        
                    if command=='new' or command=='Q':
                        speak("Instance ended, type \"start\" to continue")
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
        print("To encode the image : \n img-encode")
        print("To start new instance : \n Q or new")
    
    elif zero=='speak':
        sjson()
        print("restart the program to see changes")
        raise DeprecationWarning
        

    else:
            pass

if __name__=='__main__':
    jfunc()
    try :
        with open('speak.json') as jsonfile:
            adres = jsonfile.read()

        adres=adres.replace('{"speak": "','' )
        adres=adres.replace('"}','' )
        adres=adres.replace('"','' )
        if adres=="false":
            print("WELCOME {VOICE : DEACTIVATED}")
            while True:
                print("ENTER START TO CONTINUE.[To change speak settings enter speak]")
                main()
        else:
            print("WELCOME {VOICE : ACTIVATED}")
            while True:
                speak("ENTER START TO CONTINUE.[To change speak settings enter speak]")
                mainwithspeak()
    except DeprecationWarning as d:
        pass
