from services.document_service import DocumentService
from bson import ObjectId
from model.document_reader.tag_manager.color import Color  # adjust import path if needed

if __name__ == "__main__":
    print("=== Manual Integration Test: DocumentService.mark_read/unread + add/remove favorites + delete ===")

    service = DocumentService()

    # Replace with a valid existing project ID in your DB:
    project_id = input("Enter project_id to attach document to: ").strip()

    # 1) Create a new document with dummy data
    created_doc = service.__create_document(
        name="qotsa",
        project_id=project_id,
        path="/fake/path/to/doc.pdf",
        vector_store_path="/fake/path/to/vector.store",
        author="chemistry",
        year="1973",
        journal="josh",
        pages=130,
        bibtex="@article{doe2025, title={My Test}, author={John Doe}}",
    )
    print("\n✅ Document creation attempted! Go check Compass: database 'arcai' -> collection 'documents'.")

    # 2) Start persistent loop
    while True:
        docs = service.get_project_documents(project_id)
        if not docs:
            print("\n❌ No documents found for that project.")
            break

        print(f"\nFound {len(docs)} documents in project {project_id}:")
        for i, doc in enumerate(docs, start=1):
            print(f"Document {i}: id={doc.id}, name={doc.name}, author={doc.author}, year={doc.year}, "
                  f"read={doc.is_read()}, favorite={doc.is_favorite()}")

        print("\n0) Quit")
        try:
            choice = int(input(f"\nSelect a document to act on (0-{len(docs)}): ").strip())
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            continue

        if choice == 0:
            print("✅ Exiting test script.")
            break

        if choice < 1 or choice > len(docs):
            print("❌ Invalid selection. Try again.")
            continue

        selected_doc = docs[choice - 1]
        print(f"\nSelected document ID: {selected_doc.id}, name: {selected_doc.name}")

        action = input(
            "Type 'read' to mark as read, 'unread' to mark as unread, "
            "'fav' to add to favorites, 'unfav' to remove from favorites, "
            "'delete' to delete the document: "
        ).strip().lower()
        doc_oid = ObjectId(str(selected_doc.id))

        if action == "read":
            result = service.mark_as_read(doc_oid)
            print(f"\n✅ Marked as read: {result}")
        elif action == "unread":
            result = service.mark_as_unread(doc_oid)
            print(f"\n✅ Marked as unread: {result}")
        elif action == "fav":
            result = service.add_to_favorites(doc_oid)
            print(f"\n✅ Added to favorites: {result}")
        elif action == "unfav":
            result = service.remove_from_favorites(doc_oid)
            print(f"\n✅ Removed from favorites: {result}")
        elif action == "delete":
            confirm = input("⚠️ Are you sure you want to delete this document? Type 'yes' to confirm: ").strip().lower()
            if confirm == "yes":
                result = service.delete_document(doc_oid)
                print(f"\n✅ Document deleted: {result}")
            else:
                print("❎ Deletion cancelled.")
        elif action == "tag":
            tag_name = input("Enter tag name: ").strip()
            color_name = input(f"Enter color name (choose from {', '.join([c.name for c in Color])}): ").strip().upper()
            try:
                color_value = Color[color_name].value
                result = service.add_tag(doc_oid, tag_name, color_value)
                print(f"\n✅ Tag set: name='{tag_name}', color={color_value} | Success: {result}")
            except KeyError:
                print("❌ Invalid color name. Please try again.")

        elif action == "untag":
            result = service.remove_tag(doc_oid)
            print(f"\n✅ Tag removed. Success: {result}")

        elif action == "showtag":
            tag = service.get_document_tag(doc_oid)
            if tag:
                print(f"\n📎 Current tag — Name: {tag.name}, Color: {tag.color}")
            else:
                print("ℹ️ This document has no tag.")
        else:
            print("❌ Invalid action. Try again.")
