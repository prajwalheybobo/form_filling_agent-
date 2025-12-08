from pymongo import MongoClient
from datetime import datetime

class MongoMemoryStore:
    def __init__(self, session_id):
        self.session_id = session_id
        self.collection = MongoClient("mongodb://localhost:27017") \
            .agentdb.sessions

    def load(self):
        doc = self.collection.find_one({"sessionId": self.session_id})
        if doc:
            return doc.get("history", [])
        return []

    def save(self, history):
        self.collection.update_one(
            {"sessionId": self.session_id},
            {
                "$set": {
                    "history": history,
                    "updatedAt": datetime.utcnow()
                }
            },
            upsert=True
        )

    def clear(self):
        self.collection.delete_one({"sessionId": self.session_id})
