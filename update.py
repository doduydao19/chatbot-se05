import pickle


#1. lay du lieu tu database ve
import pymysql
import json
def load_database_form_sql():
    host_name = "localhost"
    user_name = "root"
    password = ""
    database_name = "CHATBOTH3D"
    connection = pymysql.connect(host=host_name,user=user_name,passwd=password,database=database_name )
    cursor = connection.cursor()
    #load all table:
    tables = []
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'CHATBOTH3D'")
    tables_set = cursor.fetchall()
    database = []
    for table in tables_set:
        query = "select * from `"+table[0]+"`"
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        database.append((table,data))
    return database

def update_dataset(database):
    class Intent:
        def __init__(self,tag,question,answer):
            self.tag = tag
            self.question = question
            self.answer = answer

        def form_intent(self):
            intent = {
                "tag":  self.tag,
                "questions":self.question,
                "answers": self.answer,

                }
            return intent
    intents = []
    for data in database:
        tag = str(data[0][0]).lower().replace("\b","")
            #load question and answer
        question= set()
        answer =set()
        for qa in data[1]:
            print(qa)
            question.add(qa[0])
            answer.add(qa[1])

        intent = Intent(tag,list(question),list(answer)).form_intent()
        intents.append(intent)
    result={"intents": intents}
    result =json.dumps(result, ensure_ascii=False,indent=4)
    file_out = '../chatbot-se05/sql/intents1.json'
    file_out = open(file_out,"w",encoding="utf-8")
    file_out.write(result)
    file_out.close()
    print("Update data successfully")

#2 update model
from underthesea import word_tokenize
import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense,Dropout
import pickle

def buil_new_model():
    with open('../chatbot-se05/sql/intents1.json') as json_data:
        intents = json.load(json_data)

    words = []
    classes = []
    documents = []

    fileName = "../chatbot-se05/process/StopWords"
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

    pickle.dump(words, open('../chatbot-se05/sql/words.pkl', 'wb'))
    pickle.dump(classes, open('../chatbot-se05/sql/classes.pkl', 'wb'))
    pickle.dump(documents, open('../chatbot-se05/sql/documents.pkl', 'wb'))
    pickle.dump(ignore_words, open('../chatbot-se05/sql/ignore_words.pkl', 'wb'))

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
    model_path = "../chatbot-se05/sql/H3D.h5"
    model.save(model_path)

    # Evaluate the model on the test data using `evaluate`
    print("Evaluate on test data")
    results = model.evaluate(np.array(test_x), np.array(test_y), batch_size=32)
    print("test loss, test acc:", results)


# database = load_database_form_sql()
# update_dataset(database)
buil_new_model()
