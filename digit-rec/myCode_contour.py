import WebGUI
import Frequency
import onnxruntime
import numpy as np
import cv2
from model import model_path

# Load ONNX model
ort_session = onnxruntime.InferenceSession(model_path)

# Print input shape once (debugging)
print("Model input shape:", ort_session.get_inputs()[0].shape)

while True:
    image = WebGUI.getImage()

    if image is None:
        Frequency.tick()
        continue

    # Preprocess
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    pred = None
    if contours:
        
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        digit = gray[y:y+h, x:x+w]

        resized = cv2.resize(digit, (28, 28))
        normalized = resized.astype(np.float32) / 255.0
        normalized = (normalized - 0.5) / 0.5
        input_tensor = normalized[np.newaxis, np.newaxis, :, :]  

        # Inference
        outputs = ort_session.run(None, {"input": input_tensor})
        pred = int(np.argmax(outputs[0]))

        # Display prediction on frame
        cv2.putText(image, f"Predicted: {pred}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Always show the camera feed
    WebGUI.showImage(image)

    Frequency.tick()
