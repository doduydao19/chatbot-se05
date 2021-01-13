import json

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

def load_data_sql(file_sql):
    with open(file_sql) as json_data:
        data_sql = json.load(json_data)

    intents=[]

    for table in data_sql:

        if table["type"] =="table":
            tag = str(table["name"]).lower()
            #load question and answer
            question= set()
            answer =set()
            for data in table["data"]:
                question.add(data["Question"])
                answer.add(data["Answer"])

            intent = Intent(tag,list(question),list(answer)).form_intent()
            intents.append(intent)
    return intents

def wirte_intents(file_sql,file_out):

    intents = load_data_sql(file_sql)
    result={"intents": intents}
    result =json.dumps(result, ensure_ascii=False,indent=4)

    file_out = open(file_out,"w",encoding="utf-8")
    file_out.write(result)
    file_out.close()

if __name__ == '__main__':
    file_sql = '../../chatbot-se05/sql/CHATBOTH3D-1.json'
    file_intents = '../../chatbot-se05/sql/intents.json'
    wirte_intents(file_sql,file_intents)
    print("Done")
