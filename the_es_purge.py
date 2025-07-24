from database.utils.db_setup import es

# Main loop
if __name__ == '__main__':
    es.indices.delete(index="conversations")
    es.indices.create(index = "conversations", body={
            "mappings": {
                "properties": {
                    "user_id":{"type": "text"}, 
                    "name": {"type": "text"},
                    "suggest": {"type": "completion"}
                }
            }
        })
    es.indices.delete(index="documents")
    es.indices.create(index="documents", body={
            "mappings": {
                "properties": {
                    "user_id":{"type": "text"},
                    "name": {"type": "text"},
                    "author": {"type": "text"},
                    "text": {"type": "text"},
                    "suggest": {"type": "completion"}
                }
            }
        })
    print("es has been purged")
    


        