from process.preProcess import processing

file_test = open("sentences_test","r",encoding="utf-8")

sentences = file_test.readlines()

for sentence in sentences:
    sentence = processing(sentence[:-1])
    print (sentence)