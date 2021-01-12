import os
import json
import sys
path = "C:/Users/Mr.SpAm-PC/Documents/Git/SE05-Nhom23/data_raw"

class Doc:
    def __init__(self,filename):
        self.file = filename
        self.load_data_answer()
        self.load_data_question()

    def load_data_answer(self):
        filename = self.file
        file = open(filename,"r",encoding="utf-8")
        data_answer = set()
        for line in file:
            line = line.strip("\n")
            data_answer.add(line)

        answers = list(data_answer)
        answers.sort()
        return answers
    def load_data_question(self):
        filename = self.file
        file = open(filename,"r",encoding="utf-8")
        data_question = set()
        for line in file:
            line = line.strip("\n")
            data_question.add(line)

        questions = list(data_question)
        questions.sort()
        return questions

class Intent:
    def __init__(self,tag,question,answer,contexture_lv1,contexture_lv2):
        self.tag = tag
        self.question = question
        self.answer = answer
        self.contexture_lv1 = contexture_lv1
        self.contexture_lv2 = contexture_lv2

    def form_intent(self):
        intent = {
            "tag":  self.tag,
            "question":self.question,
            "answer": self.answer,
            "contexture_lv1": self.contexture_lv1,
            "contexture_lv2":self.contexture_lv2
            }
        return intent
def load_intents(path_data_raw):
    intents = []

    contextures = os.listdir(path)
    # tầng 1:
    for contexture in contextures:
        if contexture != ".DS_Store":
            # print(contexture+"\n")
            path_lv2 = path_data_raw+"/"+contexture
            # print(path_lv2)
            contextures_lv2 = os.listdir(path_lv2)

    # tầng 2:
            for contexture_lv2 in contextures_lv2:
                if contexture_lv2 != ".DS_Store":
                    path_lv3 = path_lv2+"/"+contexture_lv2
                    tags = os.listdir(path_lv3)
                    # print(tags)

    # tầng 3:
                    for tag in tags:
                        if tag != ".DS_Store":
                            # print(tag)
                            path_lv4 = path_lv3+"/"+tag
                            docs = os.listdir(path_lv4)
    # tầng 4:
                            ans = []
                            que = []
                            for doc in docs:
                                if doc != ".DS_Store":
                                    path_doc = path_lv4+"/"+doc

                                    if doc =="answer.txt":
                                        answers = Doc(path_doc)
                                        ans = answers.load_data_answer()
                                        # print(ans)
                                    else:
                                        quetions = Doc(path_doc)
                                        que = quetions.load_data_question()
                                        # print(que)

                            intent = Intent(tag,que,ans,contexture_lv2,contexture)

                            intents.append(intent)
    print("loaded!")
    return intents
def wirte_intents(path_data_raw,path_out):
    intents = load_intents(path_data_raw)
    result={"intents": [intent.form_intent() for intent in intents]}
    result =json.dumps(result, ensure_ascii=False,indent=4)
    print(result)
    file_out = open(path_out,"w",encoding="utf-8")
    file_out.write(result)
    file_out.close()
if __name__ == '__main__':
    path_data_raw = "C:/Users/Mr.SpAm-PC/Documents/Git/SE05-Nhom23/data_raw"
    path_out = "C:/Users/Mr.SpAm-PC/Documents/Git/SE05-Nhom23/dataset/intents"
    wirte_intents(path_data_raw,path_out)
