<h1 align="center">⚡ Pikachu — OCR & QR Text Tool</h1>
<p align="center">Fast. Simple. Cute. Powerful.</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="70%">
</p>


# ⚡ Pikachu — OCR & QR Text Tool

**Pikachu** is a small Python tool that can:

* extract text from images (OCR)
* read QR codes
* save text as PDF or TXT
* share text on WhatsApp
* encode images to Base64
* speak text aloud (optional)

---

## 📦 Installation

Install required packages:

```bash
pip install pillow pytesseract opencv-python pywhatkit reportlab pyttsx3
```

Install Tesseract OCR:
[https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

Pikachu will ask for the Tesseract path the first time you run it.

---

## ▶️ Run Pikachu

```bash
python main.py
```

You will see:

```
WELCOME {VOICE : ON/OFF}
ENTER START TO CONTINUE
```

---

## 🧠 Commands

**Extract text:**

```
extract text -img <path>
```

**Search text online:**

```
text -search
```

**Save text:**

```
text -save as output.pdf
text -save as output.txt
```

**Share on WhatsApp:**

```
text -share
```

**Encode image:**

```
img -encode <path>
```

**Toggle voice:**

```
speak
```

**Restart/new instance:**

```
new
Q
```

---

## 🗂️ File Info

`app.json` → stores Tesseract path
`son.json` → voice mode ON/OFF

Example:

```json
{
  "tesseract_path": "C:/Program Files/Tesseract-OCR/tesseract.exe"
}
```

```json
{
  "speak": "true"
}
```

---

## ✔️ Voice Example

If voice mode is ON, Pikachu will speak:

```
Opening web.
File saved.
Message sent.
```


