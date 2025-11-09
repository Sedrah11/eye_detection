<<<<<<< HEAD
import os
import uuid
import cv2
import threading
import webbrowser
from flask import Flask, render_template, request, redirect, url_for

# Config
UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"
ALLOWED_EXT = {"png", "jpg", "jpeg", "bmp"}


os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Load cascades 
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade  = cv2.CascadeClassifier("haarcascade_eye.xml")
if face_cascade.empty() or eye_cascade.empty():
    raise FileNotFoundError("Cascade XML files not found. Place both .xml files in the project folder.")

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RESULT_FOLDER"] = RESULT_FOLDER

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

def detect_eyes_in_image(input_path, output_path):
    
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError("Could not read image: " + input_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80,80))

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        face_gray  = gray[y:y+h, x:x+w]
        face_color = img[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(face_gray, scaleFactor=1.1, minNeighbors=10, minSize=(20,20))
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(face_color, (ex, ey), (ex+ew, ey+eh), (0,255,0), 2)

    cv2.imwrite(output_path, img)

@app.route("/", methods=["GET", "POST"])
def index():
    result_file = None
    if request.method == "POST":
        if "image" not in request.files:
            return render_template("index.html", error="No file part")

        file = request.files["image"]
        if file.filename == "":
            return render_template("index.html", error="No selected file")

        if file and allowed_file(file.filename):
            # Save upload with unique name
            ext = file.filename.rsplit(".", 1)[1].lower()
            upload_name = f"{uuid.uuid4().hex}.{ext}"
            upload_path = os.path.join(app.config["UPLOAD_FOLDER"], upload_name)
            file.save(upload_path)

            # Process and save result
            result_name = f"res_{uuid.uuid4().hex}.{ext}"
            result_path = os.path.join(app.config["RESULT_FOLDER"], result_name)
            try:
                detect_eyes_in_image(upload_path, result_path)
            except Exception as e:
                return render_template("index.html", error=f"Processing error: {e}")

            result_file = result_path.replace("\\", "/")  # for windows paths
            # Show result image on page
            return render_template("index.html", result=result_file)

        else:
            return render_template("index.html", error="File not allowed. Use png/jpg/jpeg/bmp.")

    return render_template("index.html")

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    
    threading.Timer(1.0, open_browser).start()
    
    app.run(debug=True, use_reloader=False)
=======
import os
import uuid
import cv2
import threading
import webbrowser
from flask import Flask, render_template, request, redirect, url_for

# Config
UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"
ALLOWED_EXT = {"png", "jpg", "jpeg", "bmp"}

# Make sure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Load cascades (they must be in same folder as app.py)
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade  = cv2.CascadeClassifier("haarcascade_eye.xml")
if face_cascade.empty() or eye_cascade.empty():
    raise FileNotFoundError("Cascade XML files not found. Place both .xml files in the project folder.")

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RESULT_FOLDER"] = RESULT_FOLDER

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

def detect_eyes_in_image(input_path, output_path):
    """Run face -> eye detection, save output image to output_path."""
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError("Could not read image: " + input_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80,80))

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        face_gray  = gray[y:y+h, x:x+w]
        face_color = img[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(face_gray, scaleFactor=1.1, minNeighbors=10, minSize=(20,20))
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(face_color, (ex, ey), (ex+ew, ey+eh), (0,255,0), 2)

    cv2.imwrite(output_path, img)

@app.route("/", methods=["GET", "POST"])
def index():
    result_file = None
    if request.method == "POST":
        if "image" not in request.files:
            return render_template("index.html", error="No file part")

        file = request.files["image"]
        if file.filename == "":
            return render_template("index.html", error="No selected file")

        if file and allowed_file(file.filename):
            # Save upload with unique name
            ext = file.filename.rsplit(".", 1)[1].lower()
            upload_name = f"{uuid.uuid4().hex}.{ext}"
            upload_path = os.path.join(app.config["UPLOAD_FOLDER"], upload_name)
            file.save(upload_path)

            # Process and save result
            result_name = f"res_{uuid.uuid4().hex}.{ext}"
            result_path = os.path.join(app.config["RESULT_FOLDER"], result_name)
            try:
                detect_eyes_in_image(upload_path, result_path)
            except Exception as e:
                return render_template("index.html", error=f"Processing error: {e}")

            result_file = result_path.replace("\\", "/")  # for windows paths
            # Show result image on page
            return render_template("index.html", result=result_file)

        else:
            return render_template("index.html", error="File not allowed. Use png/jpg/jpeg/bmp.")

    return render_template("index.html")

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    # Start the browser once and disable Flask reloader so we don't open multiple tabs.
    threading.Timer(1.0, open_browser).start()
    # IMPORTANT: use_reloader=False prevents Flask from starting the app twice in debug mode.
    app.run(debug=True, use_reloader=False)
>>>>>>> f0bad1404df7cb18c34a0aedad7575c471482495
