import tensorflow as tf
import matplotlib.pyplot as plt

# ============================================================
# 1. Configuration
# ============================================================

TRAIN_DIR = "data/train"
TEST_DIR = "data/test"

IMG_SIZE = (224, 224)
BATCH_SIZE = 8
NUM_CLASSES = 3

INITIAL_EPOCHS = 15
FINE_TUNE_EPOCHS = 10

SEED = 42


# ============================================================
# 2. Load Training Dataset
# ============================================================

train_dataset = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    labels="inferred",
    label_mode="categorical",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=True,
    seed=SEED,
    validation_split=0.2,
    subset="training"
)


# ============================================================
# 3. Load Validation Dataset
# ============================================================

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    labels="inferred",
    label_mode="categorical",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=True,
    seed=SEED,
    validation_split=0.2,
    subset="validation"
)


# ============================================================
# 4. Load Test Dataset
# ============================================================

test_dataset = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    labels="inferred",
    label_mode="categorical",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)


# ============================================================
# 5. Class Names
# ============================================================

class_names = train_dataset.class_names

print("\nClasses:", class_names)


# ============================================================
# 6. Prefetch
# ============================================================

AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(AUTOTUNE)
validation_dataset = validation_dataset.prefetch(AUTOTUNE)
test_dataset = test_dataset.prefetch(AUTOTUNE)


# ============================================================
# 7. Data Augmentation
# ============================================================

data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomRotation(0.05),
    tf.keras.layers.RandomZoom(0.10),
    tf.keras.layers.RandomContrast(0.10)
], name="data_augmentation")


# ============================================================
# 8. EfficientNetB0
# ============================================================

base_model = tf.keras.applications.EfficientNetB0(
    include_top=False,
    weights="imagenet",
    input_shape=(224, 224, 3)
)

# Initially freeze everything
base_model.trainable = False


# ============================================================
# 9. Build Model
# ============================================================

inputs = tf.keras.Input(
    shape=(224, 224, 3)
)

x = data_augmentation(inputs)

x = base_model(
    x,
    training=False
)

x = tf.keras.layers.GlobalAveragePooling2D()(x)

x = tf.keras.layers.Dropout(0.3)(x)

outputs = tf.keras.layers.Dense(
    NUM_CLASSES,
    activation="softmax"
)(x)

model = tf.keras.Model(
    inputs,
    outputs
)


# ============================================================
# 10. Compile - Initial Training
# ============================================================

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.001
    ),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)


# ============================================================
# 11. Callbacks
# ============================================================

checkpoint = tf.keras.callbacks.ModelCheckpoint(
    "best_document_classifier.keras",
    monitor="val_accuracy",
    save_best_only=True,
    mode="max",
    verbose=1
)

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True,
    verbose=1
)


# ============================================================
# 12. Initial Training
# ============================================================

print("\n========================================")
print("INITIAL TRAINING")
print("========================================\n")

history_initial = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=INITIAL_EPOCHS,
    callbacks=[
        checkpoint,
        early_stopping
    ]
)


# ============================================================
# 13. Fine-Tuning
# ============================================================

print("\n========================================")
print("FINE-TUNING EFFICIENTNET")
print("========================================\n")


# Unfreeze EfficientNet
base_model.trainable = True


# Freeze most layers
# Only the last 20 layers will be trainable
for layer in base_model.layers[:-20]:
    layer.trainable = False


# Recompile with VERY small learning rate
model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=1e-5
    ),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)


# ============================================================
# 14. Fine-Tune
# ============================================================

history_fine = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=FINE_TUNE_EPOCHS,
    callbacks=[
        checkpoint,
        early_stopping
    ]
)


# ============================================================
# 15. Load Best Model
# ============================================================

print("\nLoading best model...")

model = tf.keras.models.load_model(
    "best_document_classifier.keras"
)


# ============================================================
# 16. Final Test Evaluation
# ============================================================

print("\n========================================")
print("FINAL TEST EVALUATION")
print("========================================\n")

test_loss, test_accuracy = model.evaluate(
    test_dataset
)

print("Test Loss:", test_loss)
print("Test Accuracy:", test_accuracy)


# ============================================================
# 17. Save Final Model
# ============================================================

model.save(
    "document_classifier_final.keras"
)

print("\nModel saved successfully.")


# ============================================================
# 18. Plot Initial Training
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    history_initial.history["accuracy"],
    label="Training Accuracy"
)

plt.plot(
    history_initial.history["val_accuracy"],
    label="Validation Accuracy"
)

plt.xlabel("Epoch")
plt.ylabel("Accuracy")

plt.title(
    "Initial Training Accuracy"
)

plt.legend()

plt.show()


# ============================================================
# 19. Plot Fine-Tuning
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    history_fine.history["accuracy"],
    label="Fine-Tune Training Accuracy"
)

plt.plot(
    history_fine.history["val_accuracy"],
    label="Fine-Tune Validation Accuracy"
)

plt.xlabel("Epoch")
plt.ylabel("Accuracy")

plt.title(
    "Fine-Tuning Accuracy"
)

plt.legend()

plt.show()