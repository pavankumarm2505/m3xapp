
from flask import Flask, render_template, request, jsonify, Response
import cv2
import command  # Assuming command.py is in the same directory

app = Flask(__name__)

# camera = cv2.VideoCapture(0)

def gen_frames():  
    camera_index = 0
    cap = None
    while cap is None and camera_index < 10:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            cap = None
            camera_index += 1

    if cap is None:
        raise RuntimeError("Could not open video capture")

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('front.html')

# def gen_frames():
#     while True:
#         success, frame = camera.read()
#         if not success:
#             break
#         else:
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/start', methods=['POST'])
def start():
    print("Start action")
    command.start()
    return jsonify(success=True)



@app.route('/stop', methods=['POST'])
def stop():
    print("Stop action")
    command.stop()
    return jsonify(success=True)

@app.route('/reset', methods=['POST'])
def reset():
    print("Reset action")
    command.reset()
    return jsonify(success=True)

@app.route('/pause', methods=['POST'])
def pause():
    print("Pause action")
    command.pause()
    return jsonify(success=True)

@app.route('/make_cereal_bowl', methods=['POST'])
def make_cereal_bowl():
    print("Make a cereal bowl")
    command.start()  # Start the task
    
    return jsonify(success=True)

@app.route('/next_subtask', methods=['POST'])
def next_subtask():
    command.next_subtask()
    return jsonify(success=True)

@app.route('/get_subtasks', methods=['GET'])
def get_subtasks():
    subtasks, current_subtask_index = command.get_subtasks()
    return jsonify(subtasks=subtasks, current_subtask_index=current_subtask_index)     #use these commented lines when used in the main computer
    # return jsonify(success=True)

@app.route('/previous_subtask', methods=['POST'])
def previous_subtask():
    command.previous_subtask()
    return jsonify(success=True)

@app.route('/process_speech', methods=['POST'])
def process_speech():
    data = request.get_json()
    transcript = data.get('transcript', '')
    # we can process the transcript here or we can send it to command.py if we have processor already
    print("Received transcript:", transcript)
    #or we can just add the logic here
    return jsonify(success=True, message="Processed transcript: " + transcript)

if __name__ == '__main__':
    app.run(debug=True)
