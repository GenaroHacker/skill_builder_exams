# -*- coding: utf-8 -*-
"""sql.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aUVCEgoYb6at353yz0ZYxGXu5C8DCzE3
"""

#@title sql_core
import sqlite3

def create_table( database_name , table_name , table_structure ):
    my_connection=sqlite3.connect(database_name)
    my_cursor=my_connection.cursor()
    try:
        my_cursor.execute('''
            CREATE TABLE {} ( {} )
        '''.format(table_name, table_structure))
        my_connection.commit()
        my_connection.close()
        #Table created successfully
    except sqlite3.OperationalError:
        #Table already exists
        pass

def insert_record(database_name, record):
    my_connection=sqlite3.connect(database_name)
    my_cursor=my_connection.cursor()
    my_cursor.execute(record)
    my_connection.commit()
    my_connection.close()

def insert_several_records(database_name, multiple_records):
    my_connection=sqlite3.connect(database_name)
    my_cursor=my_connection.cursor()
    for i in multiple_records:
        my_cursor.execute(i)
    my_connection.commit()
    my_connection.close()

def read_records(database_name, table_name):
    my_connection=sqlite3.connect(database_name)
    my_cursor=my_connection.cursor()
    my_cursor.execute("SELECT * FROM {}".format(table_name))
    records=my_cursor.fetchall()
    my_connection.close()
    return records

def read_last_record(database_name, table_name):
    my_connection=sqlite3.connect(database_name)
    my_cursor=my_connection.cursor()
    my_cursor.execute("SELECT * FROM {} ORDER BY ID DESC LIMIT 1".format(table_name))
    records=my_cursor.fetchall()
    my_connection.close()
    return records[0]

def update_record(database_name, record):
    my_connection=sqlite3.connect(database_name)
    my_cursor=my_connection.cursor()
    my_cursor.execute(record)
    my_connection.commit()
    my_connection.close()

def remove_record(database_name, record):
    my_connection=sqlite3.connect(database_name)
    my_cursor=my_connection.cursor()
    my_cursor.execute(record)
    my_connection.commit()
    my_connection.close()

def run_command(database_name, command):
    my_connection=sqlite3.connect(database_name)
    my_cursor=my_connection.cursor()
    my_cursor.execute(command)
    my_connection.commit()
    my_connection.close()

if __name__ == "__main__":
    #Create one Table
    columns = """
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ITEM_NAME VARCHAR(50),
            PRICE INTEGER,
            SECTION VARCHAR(20)"""
    create_table("BaseProducts","TableProducts",columns)

    #Insert one record
    insert_record("BaseProducts","INSERT INTO TableProducts VALUES (NULL,'BALL',10,'SPORT')")
    #Record inserted successfully!

    #Insert several records
    insert_several_records("BaseProducts",[
        "INSERT INTO TableProducts VALUES (NULL,'GOLF STICK',25,'SPORT')",
        "INSERT INTO TableProducts VALUES (NULL,'GLASS',20,'CERAMIC')",
        "INSERT INTO TableProducts VALUES (NULL,'T-SHIRT',5,'CLOTHES')"
    ])
    #Records inserted successfully!

    #Read all records
    list_of_tuples = read_records("BaseProducts","TableProducts")

    #Read last record
    last_record = read_last_record("BaseProducts","TableProducts")

    #Update record
    update_record("BaseProducts","UPDATE TableProducts SET ITEM_NAME='BALL NAME UPDATED' WHERE ID=3")
    #The record with ID=3 has been updated successfully!

    #Remove record
    remove_record("BaseProducts","DELETE FROM TableProducts WHERE ID=3")
    #The record with ID=4 has been removed successfully!

def insert_dict_records(database_name, table_name, data_dict):
    my_connection = sqlite3.connect(database_name)
    my_cursor = my_connection.cursor()

    for question, answer in data_dict.items():
        my_cursor.execute("SELECT * FROM {} WHERE QUESTION = ? AND ANSWER = ?".format(table_name), (question, answer))
        result = my_cursor.fetchone()

        if not result:
            my_cursor.execute("INSERT INTO {} (QUESTION, ANSWER) VALUES (?, ?)".format(table_name), (question, answer))

    my_connection.commit()
    my_connection.close()
    
def read_records_as_dict(database_name, table_name):
    my_connection = sqlite3.connect(database_name)
    my_cursor = my_connection.cursor()

    my_cursor.execute("SELECT * FROM {}".format(table_name))
    records = my_cursor.fetchall()
    my_connection.close()

    result_dict = {}
    for record in records:
        id, question, answer = record
        result_dict[question] = answer

    return result_dict

def read_exam(table_name):
  return read_records_as_dict("/content/skill_builder_exams/exams.db", table_name)

def get_table_names(database_name):
    my_connection = sqlite3.connect(database_name)
    my_cursor = my_connection.cursor()
    my_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'")
    table_names = [table[0] for table in my_cursor.fetchall()]
    my_connection.close()
    return table_names
# Insert the data from the dictionary into the 'bash' table in the 'exams.db' database
def insert_exam(exam_name,exam_data={}):
  table_structure = """
      ID INTEGER PRIMARY KEY AUTOINCREMENT,
      QUESTION VARCHAR(255),
      ANSWER VARCHAR(255)
  """
  create_table("/content/skill_builder_exams/exams.db", exam_name, table_structure)
  insert_dict_records("/content/skill_builder_exams/exams.db", exam_name, exam_data)



def read_all_exams():
  exams = []
  print("tablenames: ", get_table_names("/content/skill_builder_exams/exams.db"))
  for i in get_table_names("/content/skill_builder_exams/exams.db"):
    exams.append(Exam(read_exam(i),i))
  return exams

