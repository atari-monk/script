import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist

def train_and_save_mnist_model():
    # Print TensorFlow version
    print(f"TensorFlow version: {tf.__version__}")

    # Load the MNIST dataset
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # Normalize the images to values between 0 and 1
    x_train, x_test = x_train / 255.0, x_test / 255.0

    # Reshape the data to add a channel dimension (for grayscale images)
    x_train = x_train.reshape(-1, 28, 28, 1)
    x_test = x_test.reshape(-1, 28, 28, 1)

    # Build the neural network model
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(10, activation='softmax')  # 10 classes for digits 0-9
    ])

    # Compile the model
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    # Train the model
    model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

    # Save the model to a file
    model.save("mnist_model.h5")
    print("Model saved to 'mnist_model.h5'.")

    # Evaluate the model on the test set
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
    print(f'\nTest accuracy: {test_acc}')

    # Make predictions on the test set
    predictions = model.predict(x_test)

    # Display a test image and the predicted class
    plt.imshow(x_test[0].reshape(28, 28), cmap=plt.cm.binary)
    plt.title(f"Predicted label: {predictions[0].argmax()}")
    plt.show()

def load_and_predict_mnist_model():
    # Load the saved model
    model = tf.keras.models.load_model("mnist_model.h5")
    print("Model loaded from 'mnist_model.h5'.")

    # Load the MNIST dataset again (we need it for predictions)
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # Normalize the images to values between 0 and 1
    x_test = x_test / 255.0

    # Reshape the data to add a channel dimension (for grayscale images)
    x_test = x_test.reshape(-1, 28, 28, 1)

    # Make predictions on the test set using the loaded model
    predictions = model.predict(x_test)

    # Display a test image and the predicted class
    plt.imshow(x_test[0].reshape(28, 28), cmap=plt.cm.binary)
    plt.title(f"Predicted label: {predictions[0].argmax()}")
    plt.show()
