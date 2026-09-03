import tensorflow as tf

TRAIN_DIR = "data/train"
TEST_DIR = "data/test"

IMG_SIZE = (224, 224)
BATCH_SIZE = 8
NUM_CLASSES = 3

# -----------------------------
# 1. Load training dataset
# -----------------------------

train_dataset = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    labels="inferred",
    label_mode="categorical",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=True,
    seed=42
)

# -----------------------------
# 2. Load test dataset
# -----------------------------

test_dataset = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    labels="inferred",
    label_mode="categorical",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)

class_names = train_dataset.class_names

print("Classes:", class_names)
print("Training batches:", len(train_dataset))
print("Test batches:", len(test_dataset))


# -----------------------------
# 3. Data Augmentation
# -----------------------------

data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.05),
    tf.keras.layers.RandomZoom(0.10),
    tf.keras.layers.RandomContrast(0.10)
])

print("Data augmentation created successfully.")


# -----------------------------
# 4. Load EfficientNetB0
# -----------------------------

base_model = tf.keras.applications.EfficientNetB0(
    include_top=False,
    weights="imagenet",
    input_shape=(224, 224, 3)
)

# Freeze pretrained layers
base_model.trainable = False

print("EfficientNetB0 loaded successfully.")


# -----------------------------
# 5. Build model
# -----------------------------

inputs = tf.keras.Input(shape=(224, 224, 3))

# Data augmentation
x = data_augmentation(inputs)

# EfficientNet
x = base_model(x, training=False)

# Global pooling
x = tf.keras.layers.GlobalAveragePooling2D()(x)

# Dropout
x = tf.keras.layers.Dropout(0.3)(x)

# Classification layer
outputs = tf.keras.layers.Dense(
    NUM_CLASSES,
    activation="softmax"
)(x)

model = tf.keras.Model(inputs, outputs)

model.summary()


# -----------------------------
# 6. Compile model
# -----------------------------

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

print("Model compiled successfully.")


# -----------------------------
# 6. Compile model
# -----------------------------

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

print("Model compiled successfully.")

