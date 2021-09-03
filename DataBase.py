import psycopg2

class DataBase():
    def __init__(self, database):

        try:
            self.connection = psycopg2.connect(database = database[0], user = database[1], password = database[2], host = database[3], port = database[4])
            self.cursor = self.connection.cursor()

            self.cursor.execute("CREATE TABLE IF NOT EXISTS dictionary (word1 TEXT, lang1 TEXT, word2 TEXT, lang2 TEXT)")
        except:
            raise TypeError("Connection with database cannot be established!")


    def checkData(self, data):

        for item in data:
            if not item.isalpha():
                return 1

        command = "SELECT * FROM dictionary WHERE word1 = '{}' AND lang1 = '{}' AND word2 = '{}' AND lang2 = '{}';"
        self.cursor.execute(command.format(data[0], data[1], data[2], data[3]))

        result = self.cursor.fetchall()
        if len(result) != 0:
            return 2
        
        return 0
    
    def insert(self, data):
        command = "INSERT INTO dictionary VALUES ('{}', '{}', '{}', '{}')"
        self.cursor.execute(command.format(data[0], data[1], data[2], data[3]))
        self.connection.commit()

    def searchWord(self, lst):
        command = "SELECT * FROM dictionary WHERE (word1 = '{}' AND lang1 = '{}' AND lang2 = '{}') OR (word2 = '{}' AND lang2 = '{}' AND lang1 = '{}')" 
        self.cursor.execute(command.format(lst[0], lst[1], lst[2], lst[0], lst[1], lst[2]))
        return self.cursor.fetchall()