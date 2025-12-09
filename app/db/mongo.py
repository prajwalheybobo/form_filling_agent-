from pymongo import MongoClient
from datetime import datetime

class MongoMemoryStore:
    def __init__(self, session_id):
        self.session_id = session_id
        self._client = None
        self._collection = None
    
    @property
    def collection(self):
        """Lazy initialization of MongoDB collection."""
        if self._collection is None:
            try:
                self._client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
                # Test the connection
                self._client.server_info()
                self._collection = self._client.agentdb.sessions
            except Exception as e:
                # If MongoDB is not available, raise a more informative error
                raise ConnectionError(
                    f"Failed to connect to MongoDB at mongodb://localhost:27017. "
                    f"Please ensure MongoDB is running and accessible. Error: {str(e)}"
                ) from e
        return self._collection

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
    
    def close(self):
        """Close the MongoDB connection."""
        if self._client:
            self._client.close()
            self._client = None
            self._collection = None
