import cv2
import streamlit as st
import numpy as np
import tempfile
import os

st.title("SNAPSPOT")
st.write("Tired of scrubbing through endless video to find that specific scene?")

uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
uploaded_video = st.file_uploader("Upload a video", type=["mp4"])

if uploaded_image is not None and uploaded_video is not None:
    input_image = cv2.imdecode(np.fromstring(uploaded_image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
    st.write("Input Image:")
    st.image(input_image, caption="Uploaded Image", use_column_width=True)

    # Save uploaded video to a temporary file
    temp_video_path = os.path.join(tempfile.gettempdir(), "temp_video.mp4")
    with open(temp_video_path, "wb") as temp_video_file:
        temp_video_file.write(uploaded_video.read())

    cap = cv2.VideoCapture(temp_video_path)
    st.write("Finding your Scene...")
    sift = cv2.SIFT_create()
    keypoints_input, descriptors_input = sift.detectAndCompute(input_image, None)
    bf = cv2.BFMatcher()

    occurrences = 0
    occurrence_start = 0
    occurrence_duration = 0
    prev_matches = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.write("End of video reached.")
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
                st.write(f"Occurrence {occurrences}: Start time: {occurrence_start:.2f}s, Duration: {occurrence_duration:.2f}s")
                prev_matches = []

    cap.release()
    cv2.destroyAllWindows()

