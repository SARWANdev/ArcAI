from services.document_service import DocumentService
from database.repository.document_repository import DocumentDataBase as DocumentRepository
from database.utils.db_setup import es
from datetime import datetime, timezone
from bson import ObjectId
import pytest

# Setup the DocumentService instance
service = DocumentService()

# Define some test data (you can use mock data or populate it into the test database)
users = ["alice", "bob"]
documents_by_user = {
    "alice": [
        {"name": "Trip to Japan", "author": "Anuel AA", "content": "This is a document about Japan."},
        {"name": "Ramen Recipes", "author": "Bad Bunny", "content": "This document is about ramen recipes."},
        {"name": "la jumpa", "author": "Arcangel", "content": "Y yo la vi, anda con dos"}
    ],
    "bob": [
        {"name": "Startup Ideas", "author": "Sting", "content": "This document discusses startup ideas."},
        {"name": "AI Projects", "author": "Bob Marelu", "content": "This document covers AI projects."},
        {"name": "Me gustas tu", "author": "Myke Towers", "content": "me gusta viajar me gustas tú"}
    ]
}

def choose_user():
    print("\nAvailable users:")
    for idx, user in enumerate(users, 1):
        print(f"{idx}. {user}")
    i = int(input("Choose a user (number): "))
    return users[i - 1]

# Save some documents in MongoDB and index them in Elasticsearch
def save_documents():
    for user, docs in documents_by_user.items():
        for doc in docs:
            doc_id = str(ObjectId())
            es.index(index="documents", id=doc_id, body={
                "user_id": user,
                "name": doc["name"],
                "author": doc["author"],
                "text": doc["content"], 
                "suggest": {"input": [doc["name"], doc["author"]]} 
            })

def search_documents(user_id):
    query = input("🔍 Enter a search term for documents: ")
    results = service.search_documents(user_id, query)
    if not results:
        print("No matches found.")
    else:
        print("\n🎯 Search results:")
        for r in results:
            print(f"- {r['name']}")

# Cleanup the test data
def clean_up():
    print("\n🧹 Cleaning up test data...")
    for user in users:
        es.delete_by_query(
            index="documents",
            body={"query": {"term": {"user_id": user}}},
            conflicts="proceed"
        )
    print("✅ Test data deleted from Elasticsearch.")

# Run the test
if __name__ == "__main__":
    for user in users:
        es.delete_by_query(
            index="documents",
            body={"query": {"term": {"user_id": user}}},
            conflicts="proceed"
        )
    save_documents()
    while True:
        user = choose_user()
        search_documents(user)
        again = input("\nDo you want to end the test? (y/n): ")
        if again.lower() == "y":
            break
       
    clean_up()


