# app_streamlit.py
import streamlit as st
import cv2, numpy as np
from io import BytesIO

# Load cascades (must be in repo root)
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade  = cv2.CascadeClassifier("haarcascade_eye.xml")
if face_cascade.empty() or eye_cascade.empty():
    st.error("Cascade XML files not found in repo root.")
    st.stop()

st.title("Eye Detection — Upload an image")
uploaded = st.file_uploader("Choose an image", type=["png","jpg","jpeg","bmp"])

def detect_bytes(b):
    n = np.frombuffer(b, np.uint8)
    img = cv2.imdecode(n, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(80,80))
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        fg = gray[y:y+h, x:x+w]
        fc = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(fg,1.1,10,minSize=(20,20))
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(fc,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

if uploaded:
    data = uploaded.read()
    try:
        out = detect_bytes(data)
        st.image(out, use_column_width=True, caption="Detected (blue=face, green=eyes)")
        # offer download
        _, buf = cv2.imencode(".jpg", cv2.cvtColor(out, cv2.COLOR_RGB2BGR))
        st.download_button(
            "Download result",
            BytesIO(buf.tobytes()),
            file_name="detected.jpg",
            mime="image/jpeg"
        )
    except Exception as e:
        st.error(f"Error processing image: {e}")
