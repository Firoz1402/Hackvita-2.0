import cv2


def detect_keypoints_and_descriptors(image):
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(image, None)
    return keypoints, descriptors


input_images = ['input_images/test1.jpg', 'input_images/test2.jpg', 'input_images/test3.jpg', 'input_images/test4.jpg']
input_data = []
for image_path in input_images:
    print(f"Loading input image: {image_path}")
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    keypoints, descriptors = detect_keypoints_and_descriptors(image)
    input_data.append({'image': image, 'keypoints': keypoints, 'descriptors': descriptors})


print("Loading video...")
cap = cv2.VideoCapture('input_video/test_video.mp4')


bf = cv2.BFMatcher()


occurrences = [0] * len(input_images)
occurrence_start = [0] * len(input_images)
occurrence_duration = [0] * len(input_images)
prev_matches = [[] for _ in range(len(input_images))]

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("End of video reached.")
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
                print(f"Occurrence of image {i + 1}: Start time: {occurrence_start[i]:.2f}s, Duration: {occurrence_duration[i]:.2f}s")
                prev_matches[i] = []

cap.release()
cv2.destroyAllWindows()

