import psycopg2

class DataBase():
    def __init__(self, database):
        self.connection = psycopg2.connect(database = database[0], user = database[1], password = database[2], host = database[3], port = database[4])
        self.cursor = self.connection.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS dictionary (word1 TEXT, lang1 TEXT, word2 TEXT, lang2 TEXT)")

    
    def insert(self, data):
        command = "INSERT INTO dictionary VALUES ('{}', '{}', '{}', '{}')"
        self.cursor.execute(command.format(data[0], data[1], data[2], data[3]))
        self.connection.commit()