from flask import Flask, render_template, Response
import cv2
import tensorflow as tf
import numpy as np
import pygame.mixer

app = Flask(__name__)
model = tf.keras.models.load_model('inceptionv3.h5')

def preprocess(frame):
    # preprocess the frame before passing it through the model
    processed_frame = cv2.resize(frame, (80, 80))
    processed_frame = np.expand_dims(processed_frame, axis=0)
    processed_frame = processed_frame / 255.0
    return processed_frame

def detect_drowsiness(frame):
    # preprocess the frame and pass it through the model
    processed_frame = preprocess(frame)
    prediction = model.predict(processed_frame)

    # check if the person is drowsy
    if prediction[0][0] > prediction[0][1]:
        pygame.mixer.music.load('alarm.wav')
        pygame.mixer.music.play()

    return frame

def generate_frames():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame = detect_drowsiness(frame)

        # encode the frame as JPEG and yield it as a multipart response
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/turnOffAlarm', methods=['POST'])
def turn_off_alarm():
    # Code to turn off the alarm goes here
    return 'Alarm turned off successfully'


if __name__ == '__main__':
    pygame.mixer.init()
    app.run(debug = True)
