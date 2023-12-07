# -*- coding: utf-8 -*-
"""submission_1_LSTM_Candra.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mXnx2LlL0dht0dmHKV3RnlA_ulkUX4Nz

**SUBMISSION PERTAMA KELAS BELAJAR PENGEMBANGAN MACHINE LEARNING**

 Nama : Candra Wali Sanjaya
>
 Perguruan Tinggi : Universitas Nasional Pasim
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('Emotion_final.csv')
df.head()

# Convert emotion categories to one-hot encoding
category = pd.get_dummies(df.Emotion)
new_df = pd.concat([df, category], axis=1)
new_df = new_df.drop(columns='Emotion')
new_df

# Extract texts and labels
texts = new_df['Text'].values
labels = new_df[['anger', 'fear', 'happy', 'love', 'sadness', 'surprise']].values

# Split the data into training and testing sets
train_texts, test_texts, train_labels, test_labels = train_test_split(texts, labels, test_size=0.2)

# Tokenize the texts
tokenizer = Tokenizer(num_words=5000, oov_token='x')
tokenizer.fit_on_texts(train_texts)
tokenizer.fit_on_texts(test_texts)
print(tokenizer.word_index)

# Convert texts to sequences and pad them
sequences_train = tokenizer.texts_to_sequences(train_texts)
sequences_test = tokenizer.texts_to_sequences(test_texts)

# Specify a fixed sequence length
max_sequence_length = 66
padded_train = pad_sequences(sequences_train, maxlen=max_sequence_length)
padded_test = pad_sequences(sequences_test, maxlen=max_sequence_length)

# Build the model
model = tf.keras.models.Sequential([
    tf.keras.layers.Embedding(input_dim=5000, output_dim=16, input_length=max_sequence_length),
    tf.keras.layers.LSTM(64),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(6, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

# Define a callback for early stopping
class myCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if logs.get('accuracy') > 0.9:
            print("\nAkurasi telah mencapai >90%!")
            self.model.stop_training = True

callbacks = myCallback()

# Train the model
hist = model.fit(
    padded_train, train_labels,
    validation_data=(padded_test, test_labels),
    epochs=50,
    batch_size=128,
    verbose=2,
    callbacks=[callbacks]
)

# Plot the model accuracy
training_accuracy = hist.history['accuracy']
validation_accuracy = hist.history['val_accuracy']
plt.plot(training_accuracy, label='Training Accuracy')
plt.plot(validation_accuracy, label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# Plot the model loss
training_loss = hist.history['loss']
validation_loss = hist.history['val_loss']
plt.plot(training_loss, label='Training Loss')
plt.plot(validation_loss, label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()