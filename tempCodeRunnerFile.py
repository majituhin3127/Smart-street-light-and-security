from flask import Flask, jsonify
import threading
import cv2
import face_recognition
import time

app = Flask(__name__)

def recognize_faces_once():
    known_face_encodings = []
    known_face_names = []

    def load_and_encode(image_path, name):
        try:
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(name)
                print(f"✅ Face loaded for {name}")
            else:
                print(f"⚠️ No face found in {name}'s image!")
        except Exception as e:
            print(f"❌ Error loading {name}'s image: {e}")

    # Load known faces
    load_and_encode(r"F:\final project\face\facer\Images\pp.jpg", "Tuhin3127")
    load_and_encode(r"F:\final project\face\facer\Images\sharukh.jpg", "Sharukh")
    load_and_encode(r"F:\final project\face\facer\Images\suman.jpeg", "suman3138")

    if not known_face_encodings:
        return "❌ No known faces loaded."

    video_capture = cv2.VideoCapture(0)
    start_time = time.time()
    found_names = []

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

            if len(face_distances) > 0:
                best_match_index = face_distances.argmin()
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

            found_names.append(name)

        if time.time() - start_time > 5:  # Run for 5 seconds
            break

    video_capture.release()
    cv2.destroyAllWindows()

    if found_names:
        return f"✅ Faces recognized: {set(found_names)}"
    else:
        return "😕 No face detected."

@app.route('/face_recognition', methods=['POST'])
def trigger_recognition():
    def run_recognition():
        global result_message
        result_message = recognize_faces_once()

    recognition_thread = threading.Thread(target=run_recognition)
    recognition_thread.start()
    recognition_thread.join()  # Wait for it to finish

    return jsonify({
        "status": "success",
        "message": result_message
    })

if __name__ == '__main__':
    app.run(debug=True)
