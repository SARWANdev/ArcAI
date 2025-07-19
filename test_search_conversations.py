from database.repository.conversation_repository import ConversationRepository
from services.conversation_service import ConversationService
from datetime import datetime, timezone
from bson import ObjectId
from database.utils.mongo_connector import mongo_connection
from database.utils.db_setup import es

service = ConversationService()

# Define users and sample conversation titles
users = ["alice", "bob", "carla"]

conversations_by_user = {
    "alice": ["Trip to Japan", "Ramen Recipes", "Personal Diary"],
    "bob": ["Startup Ideas", "Workout Plan", "AI Projects"],
    "carla": ["Guitar Lessons", "Book List", "Trip to Peru"]
}

# Save conversations in MongoDB and index in Elasticsearch
def save_chats():
    for user, titles in conversations_by_user.items():
        for title in titles:
            conv_id = str(ObjectId())
            conversation_data = {
                "_id": conv_id,
                "user_id": user,
                "name": title,
                "messages": [],
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc)
            }
            service.create_conversation(

                name=title,
                user_id=user
                )
            #ConversationRepository.add_to_history(conversation_data)

# === Interactive CLI ===

def choose_user():
    print("\nAvailable users:")
    for idx, user in enumerate(users, 1):
        print(f"{idx}. {user}")
    i = int(input("Choose a user (number): "))
    return users[i - 1]

def show_user_conversations(user_id):
    print(f"\n📚 Conversation history for {user_id}:")
    history = service.get_conversation_history(user_id)
    if not history:
        print("No conversations found.")
        return []
    for conv in history:
        print(f"- {conv.name}")
    return history

def search_conversations(user_id):
    query = input("🔍 Enter a search term for conversation names: ")
    results = service.search_conversations(user_id, query)
    if not results:
        print("No matches found.")
    else:
        print("\n🎯 Search results:")
        for r in results:
            print(f"- {r['name']}")

def clean_up():
    print("\n🧹 Cleaning up test data...")
    with mongo_connection() as db:
        for user in users:
            db.conversations.delete_many({"user_id": user})
            es.delete_by_query(
                index="conversations",
                body={"query": {"term": {"user_id": user}}},
                conflicts="proceed"
            )
    print("✅ Test data deleted from MongoDB and Elasticsearch.")

# Main loop
if __name__ == '__main__':
    for user in users:
            service.delete_all_chats(user)
    save_chats()
    while True:
        user = choose_user()
        show_user_conversations(user)
        search_conversations(user)
        again = input("\nDo you want to end the test? (y/n): ")
        if again.lower() == "y":
            break
    clean_up()


        