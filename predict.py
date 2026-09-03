import tensorflow as tf
import numpy as np
import os

# -----------------------------
# 1. Load trained model
# -----------------------------
model = tf.keras.models.load_model("document_classifier_final.keras")

# Class names - IMPORTANT
class_names = ["aadhar", "dl", "pan"]

# Image size used during training
IMG_SIZE = (224, 224)


# -----------------------------
# 2. Prediction function
# -----------------------------
def predict_document(image_path):

    # Load image
    image = tf.keras.utils.load_img(
        image_path,
        target_size=IMG_SIZE
    )

    # Convert image to array
    image_array = tf.keras.utils.img_to_array(image)

    # Add batch dimension
    image_array = tf.expand_dims(image_array, axis=0)

    # Predict
    predictions = model.predict(image_array, verbose=0)

    # Get highest probability class
    predicted_index = np.argmax(predictions[0])

    predicted_class = class_names[predicted_index]

    confidence = predictions[0][predicted_index] * 100

    return predicted_class, confidence


# -----------------------------
# 3. Test all test images
# -----------------------------

test_folder = "data/test"

for document_class in class_names:

    folder_path = os.path.join(test_folder, document_class)

    for image_name in os.listdir(folder_path):

        image_path = os.path.join(folder_path, image_name)

        predicted_class, confidence = predict_document(image_path)

        print("--------------------------------")
        print("Actual Document:", document_class)
        print("Image:", image_name)
        print("Predicted Document:", predicted_class)
        print("Confidence:", round(confidence, 2), "%")