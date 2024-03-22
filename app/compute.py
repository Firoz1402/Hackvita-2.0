from flask import Flask, request, jsonify
import cv2
import numpy as np
import tempfile
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to SIFT Feature Matching API"

@app.route('/process', methods=['POST'])
def process():
    uploaded_image = request.files['image']
    uploaded_video = request.files['video']

    if uploaded_image.filename == '' or uploaded_video.filename == '':
        return jsonify({"error": "Please provide both image and video files."}), 400

    input_image = cv2.imdecode(np.frombuffer(uploaded_image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

    # Save uploaded video to a temporary file
    temp_video_path = os.path.join(tempfile.gettempdir(), "temp_video.mp4")
    uploaded_video.save(temp_video_path)

    cap = cv2.VideoCapture(temp_video_path)

    sift = cv2.SIFT_create()
    keypoints_input, descriptors_input = sift.detectAndCompute(input_image, None)
    bf = cv2.BFMatcher()

    occurrences = 0
    occurrence_start = 0
    occurrence_duration = 0
    prev_matches = []

    result = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        keypoints_frame, descriptors_frame = sift.detectAndCompute(frame_gray, None)

        matches = bf.knnMatch(descriptors_input, descriptors_frame, k=2)

        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

        if len(good_matches) >= 6:
            if not prev_matches:
                occurrence_start = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                occurrences += 1

            prev_matches = good_matches
            occurrence_duration = (cap.get(cv2.CAP_PROP_POS_MSEC) / 1000) - occurrence_start
        else:
            if prev_matches:
                result.append({
                    "occurrence": occurrences,
                    "start_time": occurrence_start,
                    "duration": occurrence_duration
                })
                prev_matches = []

    cap.release()
    cv2.destroyAllWindows()

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

