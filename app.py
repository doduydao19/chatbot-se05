from underthesea import word_tokenize
import numpy as np
import random
from tensorflow import keras
from keras.models import load_model
import json
import pickle
from flask import Flask, request
import os
import requests
import pymysql

with open('intents.json') as json_data:
    intents = json.load(json_data)

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
documents= pickle.load(open('documents.pkl', 'rb'))
ignore_words = pickle.load(open('ignore_words.pkl', 'rb'))

model = load_model('model_h3d.h5')


def clean_up_sentence(sentence):

    sentence_words = word_tokenize(sentence)
    sentence_words = [word.lower() for word in sentence_words if len(word) > 1]
    return sentence_words

def bow(sentence, words, show_details=False):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)

    return (np.array(bag))

context = {}

ERROR_THRESHOLD = 0.65

def classify(sentence):
    p = bow(sentence, words)
    d = len(p)
    f = len(documents) - 2
    a = np.zeros([f, d])
    tot = np.vstack((p, a))

    results = model.predict(tot)[0]

    results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    return return_list

def response(sentence, userID, show_details=False):
    results = classify(sentence)
    print('Result:',results)
    tag = results[0][0]
    tag = "T"+tag[1:]
    retrive = "SELECT * FROM `%s`;"%tag
    answers = database_select(retrive)

    answer = random.choice(answers)
    # print(answer)
    return answer
    # # if we have a classification then find the matching intent tag
    # if results:
    #     # loop as long as there are matches to process
    #     while results:
    #         for i in intents['intents']:
    #             # find a tag matching the first result
    #             if i['tag'] == results[0][0]:
    #                 # set context for this intent if necessary
    #                 if 'contexture_lv1' in i:
    #                     if show_details: print('context:', i['contexture_lv1'] ,",", i['contexture_lv2'])
    #                     context[userID] = i['contexture_lv1']
    #                 if not 'contexture_lv1' in i or \
    #                         (userID in context and 'contexture_lv1' in i and i['contexture_lv1'] == context[userID]):
    #                     if show_details: print('tag:', i['tag'])
    #                     return (random.choice(i['answers']))
    #         results.pop(0)

#sql

host_name = "localhost"
user_name = "root"
password = ""
database_name = "CHATBOTH3D"
connection = pymysql.connect(host=host_name,user=user_name,passwd=password,database=database_name )
cursor = connection.cursor()

def database_insert(statement_query):
    cursor.execute(statement_query)
    connection.commit()

def database_select(statement_query):
    cursor.execute(statement_query)
    rows = cursor.fetchall()
    answers = []
    for row in rows:
        # print(row)
        answers.append(row[1])
    #commiting the connection then closing it.
    connection.commit()
    return answers

def database_update(statement_query):
    cursor.execute(statement_query)

def database_delete(statement_query):
    cursor.execute(statement_query)

print(response("render facebook ?", "123", show_details=True))

# app = Flask(__name__)
#
#
# @app.route('/', methods=['GET'])
# def verify():
#     # when the endpoint is registered as a webhook, it must echo back
#     # the 'hub.challenge' value it receives in the query arguments
#     if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
#         if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
#             return "Verification token mismatch", 403
#         return request.args["hub.challenge"], 200
#
#     return "Xin chào, đây là Đạo Đỗ Duy", 200
#
#
# @app.route('/', methods=['POST'])
# def webhook():
#
#     # endpoint for processing incoming messaging events
#     data = request.get_json()
#     print(data)  # you may not want to log every incoming message in production, but it's good for testing
#
#     if data["object"] == "page":
#
#         for entry in data["entry"]:
#             for messaging_event in entry["messaging"]:
#
#                 if messaging_event.get("message"):  # someone sent us a message
#
#                     sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
#                     recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
#                     message_text = messaging_event["message"]["text"]  # the message's text
#
#                     responseai = response(message_text, sender_id)
#                     send_message(sender_id, responseai)
#
#
#                 if messaging_event.get("delivery"):  # delivery confirmation
#                     pass
#
#                 if messaging_event.get("optin"):  # optin confirmation
#                     pass
#
#                 if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
#                     pass
#
#     return "ok", 200
#
#
# def send_message(recipient_id, message_text):
#
#     print("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
#
#     params = {
#         "access_token": os.environ["PAGE_ACCESS_TOKEN"]
#     }
#     headers = {
#         "Content-Type": "application/json"
#     }
#     data = json.dumps({
#         "recipient": {
#             "id": recipient_id
#         },
#         "message": {
#             "text": message_text
#         }
#     })
#     r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
#     if r.status_code != 200:
#         print(r.status_code)
#         print(r.text)
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
