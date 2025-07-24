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
    print("done")
    


        