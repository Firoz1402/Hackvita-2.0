import cv2
import streamlit as st
import tempfile
import os
import numpy as np


def detect_keypoints_and_descriptors(image):
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(image, None)
    return keypoints, descriptors

def main():
    st.title("SnapSpot")
    st.write("Tired of scrubbing through endless video to find that specific scene?")
    
    uploaded_images = st.file_uploader("Upload Images", type=["jpg", "jpeg"], accept_multiple_files=True)
    uploaded_video = st.file_uploader("Upload Video", type=["mp4"])
    
    if uploaded_images and uploaded_video:
        input_images = [cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR) for image in uploaded_images]
        input_data = []
        for image in input_images:
            keypoints, descriptors = detect_keypoints_and_descriptors(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
            input_data.append({'image': image, 'keypoints': keypoints, 'descriptors': descriptors})

        
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_video.read())
            video_path = tmp_file.name

        cap = cv2.VideoCapture(video_path)
        bf = cv2.BFMatcher()

        occurrences = [0] * len(input_images)
        occurrence_start = [0] * len(input_images)
        occurrence_duration = [0] * len(input_images)
        prev_matches = [[] for _ in range(len(input_images))]

        st.header("Uploaded Images")
        for image in input_images:
            st.image(image, caption='Uploaded Image', use_column_width=True)
        st.write("Finding Your Scene....")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.write("End of video reached.")
                break
            
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            for i, input_item in enumerate(input_data):
                keypoints_input = input_item['keypoints']
                descriptors_input = input_item['descriptors']
        
                keypoints_frame, descriptors_frame = detect_keypoints_and_descriptors(frame_gray)
        
                matches = bf.knnMatch(descriptors_input, descriptors_frame, k=2)
        
                good_matches = []
                for m, n in matches:
                    if m.distance < 0.75 * n.distance:
                        good_matches.append(m)
        
                if len(good_matches) >= 6:
                    if not prev_matches[i]:
                        occurrence_start[i] = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                        occurrences[i] += 1
        
                    prev_matches[i] = good_matches
                    occurrence_duration[i] = (cap.get(cv2.CAP_PROP_POS_MSEC) / 1000) - occurrence_start[i]
                else:
                    if prev_matches[i]:
                        st.write(f"Occurrence of image {i + 1}: Start time: {occurrence_start[i]:.2f}s, Duration: {occurrence_duration[i]:.2f}s")
                        prev_matches[i] = []

        cap.release()
        os.remove(video_path)

if __name__ == "__main__":
    main()

