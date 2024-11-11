import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from sklearn.preprocessing import LabelEncoder

# Load your trained model
model = load_model('gesture_model.keras')

# Define the LabelEncoder and fit it to your gesture labels
gestures = ['yes', 'please', 'help']
label_encoder = LabelEncoder()
label_encoder.fit(gestures)

# Preprocess function for each frame
def preprocess_frame(frame, target_size=(64, 64)):
    frame_resized = cv2.resize(frame, target_size)  # Resize to target size
    frame_array = img_to_array(frame_resized) / 255.0  # Normalize pixel values to [0, 1]
    frame_array = np.expand_dims(frame_array, axis=0)  # Add batch dimension
    return frame_array

# Open a connection to the webcam
cap = cv2.VideoCapture(0)  # 0 is the default webcam

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the frame for prediction
    preprocessed_frame = preprocess_frame(frame)

    # Predict gesture
    predictions = model.predict(preprocessed_frame)
    predicted_index = np.argmax(predictions, axis=1)[0]
    gesture = label_encoder.inverse_transform([predicted_index])[0]

    # Display the prediction on the frame
    cv2.putText(frame, f"Gesture: {gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Gesture Recognition', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()