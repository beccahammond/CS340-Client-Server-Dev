# Becca Hammond
# CS340 Module 5 Project 1
# 10/5/2025

from pymongo import MongoClient 
# from bson.objectid import ObjectId 
from pymongo.errors import PyMongoError
from typing import Any, Dict

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self,
                 user: str,
                 password: str,
                 host: str = 'localhost',
                 port: int = 27017,
                 db_name: str = 'aac',
                 collection_name: str = 'animals'):
        
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        USER = user
        PASS = password
        HOST = host
        PORT = port
        DB   = db_name
        COL  = collection_name
        # 
        # Initialize Connection 
        # 
        self.client     = MongoClient(f'mongodb://{USER}:{PASS}@{HOST}:{PORT}')
        self.database   = self.client[DB]
        self.collection = self.database[COL]

    # Create a method to return the next available record number for use in the create method
            
    # Implement the C Create in CRUD. Insert a single document. Returns True if insert succeeds, False otherwise.
    # nput argument to function will be a set of key/value pairs in the data type acceptable to the MongoDB driver insert API call
    def create(self, document: dict) -> bool: 
        
        if not isinstance(document, dict) or not document:
            raise ValueError("`document` must be a non-empty dict")

        try:
            result = self.collection.insert_one(document)
            return bool(result.inserted_id)
        except PyMongoError:
            return False

    # Create method to implement the R Read in CRUD.
    # Input arguments to function should be the key/value lookup pair to use with the MongoDB driver find API call
    def read(self, query: dict) -> list:
        """
        Retrieve documents matching the query from the collection.
        Returns a list of documents or an empty list on failure.
        """
        if not isinstance(query, dict):
            raise ValueError("`query` must be a dict")

        # Return result in a list if the command is successful, else an empty list.
        try:
            # use find() and the MongoDB cursor returned by the find() method.
            cursor = self.collection.find(query) 
            return list(cursor)
        except PyMongoError:
            return []
        
        # --- add this helper if you want to safely coerce queries ---
    @staticmethod
    def _ensure_dict(d: Dict[str, Any], name: str) -> Dict[str, Any]:
        if not isinstance(d, dict):
            raise ValueError(f"`{name}` must be a dict")
        return d

    # Update matching documents (returns the number modified)
    # query: MongoDB filter dict (e.g., {"name": "Lucy"})
    # new_values: fields to set (e.g., {"outcome_type": "Adoption"})
    # many: True -> update_many, False -> update_one
    def update(self, query: dict, new_values: dict, many: bool = True) -> int:
        query = self._ensure_dict(query, "query")
        new_values = self._ensure_dict(new_values, "new_values")
        if not new_values:
            raise ValueError("`new_values` must be a non-empty dict")

        try:
            if many:
                result = self.collection.update_many(query, {"$set": new_values})
            else:
                result = self.collection.update_one(query, {"$set": new_values})
            return int(result.modified_count)
        except PyMongoError:
            return 0

    # Delete matching documents (returns the number deleted)
    # query: MongoDB filter dict (e.g., {"rec_num": 123})
    # many: True -> delete_many, False -> delete_one
    def delete(self, query: dict, many: bool = True) -> int:
        query = self._ensure_dict(query, "query")
        try:
            if many:
                result = self.collection.delete_many(query)
            else:
                result = self.collection.delete_one(query)
            return int(result.deleted_count)
        except PyMongoError:
            return 0
        
        