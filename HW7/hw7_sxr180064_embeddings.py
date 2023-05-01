# -*- coding: utf-8 -*-
"""HW7_SXR180064_EMBEDDINGS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OPoUf8f2C6V67kxik3od1lJ73qFGGa7g
"""

import numpy as np
import tensorflow as tf
import pandas as pd
from tensorflow import keras
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization

df = pd.read_csv("./ecommerceDataset.csv", header=None)
df.columns = ['label', 'text']
df.head()

df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

cols = df.select_dtypes(include=['object'])
for col in cols.columns.values:
    df[col] = df[col].fillna('')

df["label"].loc[df["label"]=="Household"]=0.0
df["label"].loc[df["label"]=="Books"]=1.0
df["label"].loc[df["label"]=="Electronics"]=2.0
df["label"].loc[df["label"]=="Clothing & Accessories"]=3.0

i = np.random.rand(len(df)) < 0.8
train = df[i]
test = df[~i]
print("train data size: ", train.shape)
print("test data size: ", test.shape)

vectorizer = TextVectorization(max_tokens=20000, output_sequence_length=200)
text_ds = tf.data.Dataset.from_tensor_slices(df.text).batch(128)
vectorizer.adapt(text_ds)

voc = vectorizer.get_vocabulary()
word_index = dict(zip(voc, range(len(voc))))

from tensorflow.keras import layers

EMBEDDING_DIM = 128
MAX_SEQUENCE_LENGTH = 200

embedding_layer = layers.Embedding(len(word_index) + 1,
                            EMBEDDING_DIM,
                            input_length=MAX_SEQUENCE_LENGTH)

int_sequences_input = keras.Input(shape=(None,), dtype="int64")
embedded_sequences = embedding_layer(int_sequences_input)
x = layers.Conv1D(128, 5, activation="relu")(embedded_sequences)
x = layers.MaxPooling1D(5)(x)
x = layers.Conv1D(128, 5, activation="relu")(x)
x = layers.MaxPooling1D(5)(x)
x = layers.Conv1D(128, 5, activation="relu")(x)
x = layers.GlobalMaxPooling1D()(x)
x = layers.Dense(128, activation="relu")(x)
x = layers.Dropout(0.5)(x)
preds = layers.Dense(4, activation="softmax")(x)
model = keras.Model(int_sequences_input, preds)
model.summary()

x_train = vectorizer(np.array([[s] for s in train.text])).numpy()

y_train = np.array(train.label, dtype=np.float)

model.compile(
    loss="sparse_categorical_crossentropy", optimizer="rmsprop", metrics=["acc"]
)
model.fit(x_train, y_train, batch_size=128, epochs=5, validation_split=0.2)

from sklearn.metrics import *

test_x = vectorizer(np.array([[s] for s in test.text])).numpy()

preds = model.predict(test_x)
pred_labels = [np.argmax(p) for p in preds]

y_test = np.array(test.label, dtype=np.float)

print('accuracy score: ', accuracy_score(y_test, pred_labels))
print(classification_report(y_test, pred_labels))