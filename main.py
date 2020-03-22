from flask import Flask, render_template, Response
import io
import cv2

app = Flask(__name__)

# Video Capture mode, 0 => webcam
vc = cv2.VideoCapture(0)

# Renders the file where video will be streamed.
@app.route('/')
def index():
    return render_template('index.html')


# Implement Custom Algorithm here (on frame)
# and return new frame
def myAlgorithm(frame):
    modified_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return modified_frame


# Support function for converting frames to sequence of '.jpg' images
# Image sequence turned to a video stream
def generate_frames():
    while True:
        read_return_code, frame = vc.read()
        # myAlgorithm(..) output is consumed here
        modified_frame = myAlgorithm(frame)
        encode_return_code, image_buffer = cv2.imencode('.jpg', modified_frame)
        io_buf = io.BytesIO(image_buffer)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + io_buf.read() + b'\r\n')


# Output stream url (similar to ip camera stream on web)
@app.route('/video_feed')
def video_feed():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


# This helps in hosting stream to ip of device (accessible across server)
# Example : http://192.168.0.101:5000/
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
