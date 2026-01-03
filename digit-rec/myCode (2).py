import WebGUI
import HAL
import Frequency
import onnxruntime
import numpy as np
import cv2
from model import model_path_func

# Point to your ONNX model
model_path = model_path_func()

# Load ONNX model
ort_session = onnxruntime.InferenceSession(model_path)

while True:
    image = WebGUI.getImage()

    if image is None:
        Frequency.tick()
        continue

    # Preprocess
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (28, 28))
    normalized = resized.astype(np.float32) / 255.0
    input_tensor = normalized[np.newaxis, np.newaxis, :, :]  

    # Inference
    outputs = ort_session.run(None, {"input": input_tensor})
    pred = int(np.argmax(outputs[0]))

    # Display prediction
    cv2.putText(image, f"Predicted: {pred}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    WebGUI.showImage(image)
    Frequency.tick()


