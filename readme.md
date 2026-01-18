# 🎨 Air Canvas

Welcome to the **Air Canvas** project! This application allows you to draw on the screen using hand gestures via your webcam.

## 🚀 Setup & Installation Guide

Project ko apne local machine par run karne ke liye neeche diye gaye steps follow karein:

### 1. Clone the Repository
Sabse pehle terminal open karein aur repository ko clone karein:

```bash
git clone [https://github.com/divyyadav007/AirCanvas.git]
```
### 2. Open Project Directory
Clone hone ke baad, project folder ke andar jayein:

Bash
```
cd AirCanvas
```
### 3. Create Virtual Environment (Recommended)
Project ke liye ek isolated virtual environment banayein taaki libraries conflict na karein:

Bash
```
python -m venv venv
```
### 4. Activate Virtual Environment
Ab virtual environment ko activate karein:

For Windows:

Bash
```
venv\Scripts\activate
```
For macOS/Linux:

Bash
```
source venv/bin/activate
```
### 5. Install Dependencies
Environment activate hone ke baad, saari required libraries install karein:

Bash

pip install -r requirements.txt
(Note: Agar requirements.txt file nahi hai, toh manually opencv-python, numpy, aur mediapipe install kar lein).

### 6. Run the Application
Sab setup ho jane ke baad, project ko run karein:

Bash

python main.py
🎮 How to Use
Webcam start hone ka wait karein.

Apni index finger (pointing finger) ka use karke hawa mein draw karein.

Enjoy drawing!


---

### **Ek chhota sa tip:**
Agar tumne abhi tak `requirements.txt` file nahi banayi hai, to `venv` activate karne ke baad aur libraries install karne ke baad ye command run kar dena, taaki doosron ke liye setup aasaan ho jaye:

`pip freeze > requirements.txt`


