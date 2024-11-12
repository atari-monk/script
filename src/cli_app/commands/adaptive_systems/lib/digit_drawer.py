import tensorflow as tf
import numpy as np
import tkinter as tk
from tensorflow.keras.models import load_model
from tkinter import messagebox, simpledialog
import os
from PIL import Image

class DigitDrawer:
    def __init__(self, model_path="my_digit_model.h5"):
        # Load the pre-trained model or create a new one if it doesn't exist
        self.model = self.load_or_create_model(model_path)
        self.model.compile(optimizer='adam',
                           loss='sparse_categorical_crossentropy',
                           metrics=['accuracy'])

        self.canvas_data = np.zeros((28, 28))  # 28x28 canvas
        self.image_count = 0  # Count how many images we have saved

        # Ensure the directory to save images exists
        self.data_dir = "saved_images"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def load_or_create_model(self, model_path):
        """Load the model if it exists, else create a new one."""
        if os.path.exists(model_path):
            print("Loading model...")
            return load_model(model_path)
        else:
            print("Creating a new model...")
            return self.create_model()

    def create_model(self):
        """Create a new model with the same architecture."""
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(10, activation='softmax')  # 10 classes for digits 0-9
        ])
        return model

    def classify_digit(self):
        """Classify the drawn digit and show the result."""
        image = np.array(self.canvas_data, dtype=np.uint8)
        image = (image > 0).astype(np.float32)  # Convert to binary
        image = image / 255.0  # Normalize
        image = image.reshape(1, 28, 28, 1)

        prediction = self.model.predict(image)
        predicted_label = np.argmax(prediction)
        messagebox.showinfo("Prediction", f"Predicted digit: {predicted_label}")

    def save_image(self, label):
        """Save the drawn image as a PNG file."""
        image = np.array(self.canvas_data, dtype=np.uint8)
        image = (image > 0).astype(np.uint8) * 255  # Convert to black and white

        # Create the image file path
        file_path = os.path.join(self.data_dir, f"{label}_{self.image_count}.png")

        # Save the image using PIL
        img = Image.fromarray(image)
        img.save(file_path)

        # Save the image label
        with open(os.path.join(self.data_dir, "labels.txt"), "a") as f:
            f.write(f"{file_path} {label}\n")

        self.image_count += 1
        messagebox.showinfo("Image Saved", f"Image saved as {file_path}")

    def clear_canvas(self):
        """Clear the canvas."""
        self.canvas.delete("all")
        self.canvas_data = np.zeros((28, 28))

    def draw(self, event):
        """Update the canvas data when drawing."""
        x1, y1 = (event.x // 10) * 10, (event.y // 10) * 10
        self.canvas.create_oval(x1, y1, x1 + 10, y1 + 10, fill="black")
        
        row, col = y1 // 10, x1 // 10
        self.canvas_data[row, col] = 1

    def start_gui(self):
        """Initialize and start the tkinter GUI."""
        root = tk.Tk()
        root.title("Draw a Digit")

        self.canvas = tk.Canvas(root, width=280, height=280, bg="white")
        self.canvas.pack()

        classify_button = tk.Button(root, text="Classify Digit", command=self.classify_digit)
        classify_button.pack()

        save_button = tk.Button(root, text="Save Image", command=self.save_digit)
        save_button.pack()

        clear_button = tk.Button(root, text="Clear Canvas", command=self.clear_canvas)
        clear_button.pack()

        train_button = tk.Button(root, text="Train Model", command=self.train_model_button)
        train_button.pack()

        self.canvas.bind("<B1-Motion>", self.draw)

        root.mainloop()

    def save_digit(self):
        """Prompt user for the label and save the drawn digit."""
        label = simpledialog.askstring("Input", "Enter digit label (0-9):")
        if label and label.isdigit() and 0 <= int(label) <= 9:
            self.save_image(int(label))
        else:
            messagebox.showwarning("Invalid Input", "Please enter a valid digit between 0 and 9.")

    def train_model_button(self):
        """Button callback to train the model."""
        # You can specify the number of epochs
        epochs = simpledialog.askinteger("Train Model", "Enter number of epochs for training:", minvalue=1, maxvalue=20)
        if epochs:
            self.train_model(epochs)

    def train_model(self, epochs=5):
        """Train the model on the saved images."""
        image_files, labels = self.load_training_data()

        # Load images and labels
        images = [self.load_image(file) for file in image_files]
        images = np.array(images) / 255.0  # Normalize images
        images = images.reshape(-1, 28, 28, 1)

        # Train the model
        self.model.fit(images, np.array(labels), epochs=epochs)

        # Save the trained model
        self.model.save("my_digit_model.h5")
        messagebox.showinfo("Training Complete", "Model trained and saved.")

    def load_training_data(self):
        """Load the training data from saved images."""
        image_files = []
        labels = []
        with open(os.path.join(self.data_dir, "labels.txt"), "r") as f:
            for line in f:
                path, label = line.strip().split()
                image_files.append(path)
                labels.append(int(label))
        return image_files, labels

    def load_image(self, file_path):
        """Load an image from file and resize to 28x28."""
        img = Image.open(file_path).convert('L')
        img = img.resize((28, 28))
        return np.array(img)
