"""
Fashion-MNIST Model Trainer and Classifier for E-commerce Product Images (step1_eda).
Uses TensorFlow/Keras Sequential model trained on 10 fashion garment classes.
Includes 'noclothes' fallback for non-clothing/missing/invalid images.
"""

import os
import gzip
import numpy as np
import cv2
from PIL import Image
import tensorflow as tf
from tensorflow import keras

# 1. Define the 10 category labels (matches Fashion-MNIST training)
class_names = [
    'T-shirt/top',
    'Trouser',
    'Pullover',
    'Dress',
    'Coat',
    'Sandal',
    'Shirt',
    'Sneaker',
    'Bag',
    'Ankle boot'
]

FASHION_MNIST_CLASSES = {i: name for i, name in enumerate(class_names)}

MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "fashion_mnist_model.keras"))
WEIGHTS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "fashion_mnist_weights.weights.h5"))
CACHE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".keras", "datasets", "fashion-mnist"))

# Mapping from GLAMI categories to closest Fashion MNIST class for verification
GLAMI_CATEGORY_MAPPING = {
    "dresses": "Dress",
    "girls-dresses": "Dress",
    "womens-tops-tank-tops-and-t-shirts": "T-shirt/top",
    "mens-t-shirts-and-tank-tops": "T-shirt/top",
    "boys-t-shirts": "T-shirt/top",
    "womens-blouses-and-shirts": "Shirt",
    "mens-shirts": "Shirt",
    "boys-shirts": "Shirt",
    "womens-sweaters": "Pullover",
    "mens-sweaters": "Pullover",
    "womens-sweatshirts": "Pullover",
    "mens-sweatshirts": "Pullover",
    "boys-sweaters": "Pullover",
    "womens-coats": "Coat",
    "mens-coats": "Coat",
    "womens-bathrobes": "Coat",
    "mens-bath-robes": "Coat",
    "mens-sport-jackets": "Coat",
    "womens-sport-jackets": "Coat",
    "womens-pants": "Trouser",
    "mens-pants": "Trouser",
    "women-s-shorts": "Trouser",
    "mens-short": "Trouser",
    "boys-shorts": "Trouser",
    "boys-pants": "Trouser",
    "panties-and-thongs": "Trouser",
    "womens-hosiery": "Trouser",
    "womens-jumpsuits": "Dress",
    "womens-sandals": "Sandal",
    "mens-sandals": "Sandal",
    "womens-flip-flops": "Sandal",
    "mens-flip-flops": "Sandal",
    "womens-slides": "Sandal",
    "mens-slides": "Sandal",
    "womens-espadrilles": "Sandal",
    "mens-espadrilles": "Sandal",
    "heels": "Sandal",
    "womens-sneakers": "Sneaker",
    "mens-sneakers": "Sneaker",
    "boys-shoes": "Sneaker",
    "girls-shoes": "Sneaker",
    "men-dress-shoes": "Sneaker",
    "women-dress-shoes": "Sneaker",
    "mens-outdoor-shoes": "Sneaker",
    "womens-outdoor-shoes": "Sneaker",
    "mens-boots": "Ankle boot",
    "womens-boots-and-booties": "Ankle boot",
    "mens-snow-boots": "Ankle boot",
    "womens-snow-boots": "Ankle boot",
    "handbags": "Bag",
    "shoulder-bags": "Bag",
    "mens-bags": "Bag",
    "womens-backpacks": "Bag",
    "mens-backpacks": "Bag",
    "womens-wallets": "Bag",
    "mens-wallets": "Bag",
    "mens-watches": "Bag",
    "womens-watches": "Bag",
    "womens-earrings": "Bag",
    "corsets-and-garter-belts": "T-shirt/top",
    "bikinis": "T-shirt/top",
    "womens-bras": "T-shirt/top",
    "mens-undergarments": "Trouser",
    "underwear-sets": "T-shirt/top",
    "womens-shawls-and-scarves": "Coat",
    "womens-skirts": "Dress"
}

def load_fashion_mnist_data():
    """Loads Fashion-MNIST dataset from local cache or keras datasets."""
    files = [
        "train-labels-idx1-ubyte.gz",
        "train-images-idx3-ubyte.gz",
        "t10k-labels-idx1-ubyte.gz",
        "t10k-images-idx3-ubyte.gz",
    ]
    paths = [os.path.join(CACHE_DIR, f) for f in files]
    
    if all(os.path.exists(p) for p in paths):
        with gzip.open(paths[0], "rb") as lbpath:
            y_train = np.frombuffer(lbpath.read(), np.uint8, offset=8)
        with gzip.open(paths[1], "rb") as imgpath:
            x_train = np.frombuffer(imgpath.read(), np.uint8, offset=16).reshape(len(y_train), 28, 28)
        with gzip.open(paths[2], "rb") as lbpath:
            y_test = np.frombuffer(lbpath.read(), np.uint8, offset=8)
        with gzip.open(paths[3], "rb") as imgpath:
            x_test = np.frombuffer(imgpath.read(), np.uint8, offset=16).reshape(len(y_test), 28, 28)
        return (x_train, y_train), (x_test, y_test)
    else:
        return keras.datasets.fashion_mnist.load_data()

def build_model() -> keras.Model:
    """
    Builds the Sequential neural network model for Fashion-MNIST classification.
    """
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

def train_or_load_model(epochs: int = 5) -> keras.Model:
    """
    Loads trained weights/model if available, otherwise trains the Sequential model on Fashion-MNIST.
    """
    model = build_model()
    
    if os.path.exists(MODEL_PATH):
        try:
            print(f"Loading existing Fashion MNIST model from {MODEL_PATH}...")
            loaded_model = keras.models.load_model(MODEL_PATH)
            return loaded_model
        except Exception:
            pass

    if os.path.exists(WEIGHTS_PATH):
        try:
            print(f"Loading pre-trained weights from {WEIGHTS_PATH}...")
            model.load_weights(WEIGHTS_PATH)
            return model
        except Exception:
            pass

    print("Training Fashion-MNIST Sequential model on fashion_mnist dataset...")
    (x_train, y_train), (x_test, y_test) = load_fashion_mnist_data()

    # Normalize pixel values from [0, 255] to [0.0, 1.0]
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0

    model.fit(
        x_train, y_train,
        epochs=epochs,
        batch_size=128,
        validation_data=(x_test, y_test),
        verbose=1
    )

    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
    print(f"Fashion-MNIST Test Accuracy: {test_acc:.4f}")

    try:
        model.save(MODEL_PATH)
        model.save_weights(WEIGHTS_PATH)
        print(f"Model saved to {MODEL_PATH} and weights to {WEIGHTS_PATH}")
    except Exception as e:
        print(f"Note: Could not save model file: {e}")

    return model

def preprocess_custom_image(img_path: str) -> np.ndarray | None:
    """
    Loads and preprocesses custom e-commerce product image:
    1. Read image in grayscale (cv2.IMREAD_GRAYSCALE)
    2. Resize to 28x28 pixels
    3. Invert colors if background is white/light and clothing is dark
    4. Normalize pixel values from [0, 255] to [0.0, 1.0]
    """
    if not os.path.exists(img_path):
        return None
        
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None

    h, w = img.shape
    
    # Invert colors if background is light (Fashion-MNIST has black background and white clothing shapes)
    corner_size = max(5, min(h, w) // 15)
    corners = [
        img[0:corner_size, 0:corner_size],
        img[0:corner_size, w-corner_size:w],
        img[h-corner_size:h, 0:corner_size],
        img[h-corner_size:h, w-corner_size:w]
    ]
    bg_mean = np.mean([np.mean(c) for c in corners])
    
    if bg_mean > 128:
        img_inverted = cv2.bitwise_not(img)
    else:
        img_inverted = img

    # Resize to 28x28 pixels
    img_resized = cv2.resize(img_inverted, (28, 28), interpolation=cv2.INTER_AREA)

    # Normalize pixel values from [0, 255] to [0.0, 1.0]
    img_normalized = img_resized.astype("float32") / 255.0
    return img_normalized

def classify_product_image(model: keras.Model, image_path: str, category_name: str = "") -> dict:
    """
    Predicts product_class_name for custom product image using trained Fashion-MNIST Sequential model.
    If no valid image or no clothes class is found, returns product_class_name: 'noclothes'.
    """
    img_norm = preprocess_custom_image(image_path)
    
    # Fallback if image missing, corrupted, or no clothes class
    if img_norm is None:
        return {
            "class_id": -1,
            "clothes_class_name_word": "noclothes",
            "product_class_name": "noclothes",
            "confidence": 0.0
        }

    # Prepare batch of shape (1, 28, 28)
    x_custom = np.expand_dims(img_norm, axis=0)
    
    preds = model.predict(x_custom, verbose=0)[0]
    predicted_index = int(np.argmax(preds))
    confidence = float(np.max(preds))
    predicted_label = class_names[predicted_index]

    # Category name alignment if mapped
    cat_lower = str(category_name).lower().strip()
    mapped_name = GLAMI_CATEGORY_MAPPING.get(cat_lower)
    
    # Set final class name: if confidence is solid or category aligns
    final_class_name = predicted_label
    if mapped_name and confidence < 0.60:
        final_class_name = mapped_name

    return {
        "class_id": predicted_index,
        "clothes_class_name_word": final_class_name,
        "product_class_name": final_class_name,
        "confidence": round(confidence * 100, 2)
    }

if __name__ == "__main__":
    m = train_or_load_model()
    print("Model ready:", m.summary())
