from flask import Flask,Response,render_template
import cv2
url='http://192.168.0.4:8080/video'
app=Flask(__name__)
#camera = VideoStream(src=0).start()
time.sleep(2.0)
@app.route('/')
def index():
    return render_template('index.html')
    
def gen_frames():
    camera = cv2.VideoCapture(url)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__=='__main__':
    app.run(debug=True)
