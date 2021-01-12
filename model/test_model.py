from time import sleep
import numpy as np
import random
from keras.models import load_model
import pickle
import json
from preProcess import processing

with open('../../chatbot-se05/dataset/intents.json') as json_data:
    intents = json.load(json_data)
words = []
classes = []
documents = []

contexture = []

words = pickle.load(open('../../chatbot-se05/app/words.pkl', 'rb'))
classes = pickle.load(open('../../chatbot-se05/app/classes.pkl', 'rb'))
documents= pickle.load(open('../../chatbot-se05/app/documents.pkl', 'rb'))
ignore_words = pickle.load(open('../../chatbot-se05/app/ignore_words.pkl', 'rb'))


fileName = "../../chatbot-se05/process/StopWords"
file_Stop_word = open(fileName,"r",encoding="utf-8")
stopWords = set()
for line in file_Stop_word:
    line = line.strip("\n")
    stopWords.add(line)

ignore_words = list(stopWords)


for doc in documents:
    bag = []
    question_words = doc[0]
    question_words = [word.lower() for word in question_words if len(word) > 1]
    for w in words:
        if w in question_words:
            bag.append(1)
        else:
            bag.append(0)
model = load_model('../../chatbot-se05/model/H3D.h5')


def clean_up_sentence(sentence):
    sentence_words = processing(sentence).split()
    sentence_words = [word.lower() for word in sentence_words if len(word) > 1]
    return sentence_words

def bow(sentence, words, show_details=False):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))


def predict(sentence):
    p = bow(sentence, words)
    # print(p)
    # print(classes)
    #
    d = len(p)
    f = len(documents) - 2
    a = np.zeros([f, d])
    tot = np.vstack((p, a))

    prediction = model.predict(tot)
    predicted_index = np.argmax(prediction)
    # print (classes[predicted_index])

    name_class = classes[predicted_index]

    response = ""
    for intent in intents["intents"]:
        if intent["tag"] == name_class:
            contexture.append((intent['contexture_lv1'], intent['contexture_lv2']))
            response = random.choice(intent['answers'])

    # print("Câu trả lời:", response)
    return response

if __name__ == '__main__':
    question = input("User: ")
    answer = predict(question)
    print("Chatbot: ",answer)

