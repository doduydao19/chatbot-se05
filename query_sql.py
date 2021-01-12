# need install package pymysql
import pymysql
import random
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
        print(row)
        answers.append(row[1])
    #commiting the connection then closing it.
    connection.commit()
    return answers

def database_update(statement_query):
    cursor.execute(statement_query)

def database_delete(statement_query):
    cursor.execute(statement_query)

if __name__ == '__main__':

    # insert1 = "INSERT INTO Artists(NAME, TRACK) VALUES('Towang', 'Jazz' );"
    # database_insert(insert1)
    # insert2 = "INSERT INTO Artists(NAME, TRACK) VALUES('Sadduz', 'Rock' );"
    # database_insert(insert2)

    #selection:
    tag = "Chào hỏi"
    retrive = "SELECT * FROM `%s`;"%tag
    answers = database_select(retrive)

    answer = random.choice(answers)
    print(answer)

    #updateSql:
    # updateSql = "UPDATE  Artists SET NAME= 'Tauwang'  WHERE ID = '1' ;"
    # database_update(updateSql)

    #deleteSql:
    # deleteSql = "DELETE FROM Artists WHERE ID = '1'; "
    # database_delete(deleteSql)

    connection.close()
