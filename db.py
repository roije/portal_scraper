from pymongo import MongoClient

class DatabaseConnector():

    def __init__(self, database):  
        self.client = MongoClient()
        self.db = self.client[database]


    def insert_comment(self, comment_dictionary):
        comment = self.check_if_exists(comment_dictionary)
        if comment == None:
            self.db.comments.insert_one(comment_dictionary)
    

    def check_if_exists(self, comment_dictionary):
        comment = self.db.comments.find_one(
            {"text" : comment_dictionary["text"], 
            "comment_timestamp" : comment_dictionary["comment_timestamp"]})
        return comment

