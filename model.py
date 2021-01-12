from underthesea import word_tokenize
import numpy as np
import random

from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Activation,Dropout
from keras import utils
from keras import layers

import matplotlib.pyplot as plt
import pickle
import json


with open('intents.json') as json_data:
    intents = json.load(json_data)

words = []
classes = []
documents = []

fileName = "StopWords"
file_Stop_word = open(fileName,"r",encoding="utf-8")
stopWords = set()
for line in file_Stop_word:
    line = line.strip("\n")
    stopWords.add(line)

ignore_words = list(stopWords)

for intent in intents['intents']:
    for question in intent['questions']:
        w = word_tokenize(question)
        words.extend(w)
        documents.append((w, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [w.lower() for w in words if w not in ignore_words if len(w) != 1]
words = sorted(list(set(words)))

classes = sorted(list(set(classes)))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))
pickle.dump(documents, open('documents.pkl', 'wb'))
pickle.dump(ignore_words, open('ignore_words.pkl', 'wb'))

dataset = []
output = []

output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    # print(doc)
    question_words = doc[0]
    question_words = [word.lower() for word in question_words if word not in ignore_words if len(word) != 1]
    # print(question_words)
    for w in words:
        if w in question_words:
            bag.append(1)
        else:
            bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    dataset.append([bag, output_row])

    # print(bag)
random.shuffle(dataset)
len_dataset = len(dataset)

len_train = int(len_dataset * 0.8)

training = dataset[0:len_train]
testing = dataset[len_train:len_dataset]

training = np.array(training)
testing = np.array(testing)

train_x = list(training[:,0])
test_x = list(testing[:,0])

train_y = list(training[:,1])
test_y = list(testing[:,1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.6))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.6))
model.add(Dense(len(train_y[0]), activation='softmax'))
# model = Sequential()
# model.add(Dense(8, input_shape=[len(train_x[0],)]))
# model.add(Dense(8))
# model.add(Dense(8))
# model.add(Dense(len(train_y[0]), activation='softmax'))

model.summary()
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])
history = model.fit(np.array(train_x), np.array(train_y), epochs=4000, batch_size=32)

model.save('model_h3d.h5')

# Evaluate the model on the test data using `evaluate`
# print("Evaluate on test data")
# results = model.evaluate(test_x, test_y, batch_size=32)
# print("test loss, test acc:", results)



history_dict = history.history
history_dict.keys()

acc = history.history['acc']
loss = history.history['loss']
epochs = range(1, len(acc) + 1)
plt.plot(epochs, acc, 'bo', label='Training acc')

plt.title('Training and validation accuracy')
plt.legend()
plt.figure()
plt.plot(epochs, loss, 'bo', label='Training loss')
plt.title('Training and validation loss')
plt.legend()
plt.show()
