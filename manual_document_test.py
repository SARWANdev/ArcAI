import os
from bson import ObjectId
from services.document_service import DocumentService
from model.document_reader.tag_manager.color import Color  # adjust if needed

if __name__ == "__main__":
    service = DocumentService()

    # Step 1: Upload a PDF
    pdf_path = input("Enter full path to PDF file: ").strip()
    user_id = input("Enter user_id (Google sub): ").strip()
    project_id = input("Enter project_id: ").strip()

    # Step 2: Upload document using the real pipeline
    print("\nUploading document...")
    service.upload_document(
        document_path=pdf_path,
        user_id=user_id,
        project_id=project_id
    )
    print("Upload complete.\n")

    # Step 3: Loop to inspect and modify documents
    while True:
        docs = service.get_project_documents(project_id)
        if not docs:
            print("No documents found.")
            break

        print(f"\nFound {len(docs)} documents in project {project_id}:")
        for i, doc in enumerate(docs, 1):
            print(f"{i}. id={doc.document_id}, name={doc.name}, read={doc.is_read()}, fav={doc.is_favorite()}")

        print("\n0) Quit")
        try:
            choice = int(input("Select document to act on: "))
        except ValueError:
            print("⚠️ Invalid input. Try again.")
            continue

        if choice == 0:
            break
        if not (1 <= choice <= len(docs)):
            print("Out of range. Try again.")
            continue

        selected_doc = docs[choice - 1]
        doc_oid = ObjectId(str(selected_doc.document_id))

        action = input(
            "\nChoose action: read | unread | fav | unfav | tag | untag | showtag | bibtex | delete\n> "
        ).strip().lower()

        if action == "read":
            print("✔️ Marked as read:", service.mark_as_read(doc_oid))
        elif action == "unread":
            print("✔️ Marked as unread:", service.mark_as_unread(doc_oid))
        elif action == "fav":
            print("✔️ Added to favorites:", service.add_to_favorites(doc_oid))
        elif action == "unfav":
            print("✔️ Removed from favorites:", service.remove_from_favorites(doc_oid))
        elif action == "tag":
            tag = input("Tag name: ").strip()
            color = input(f"Color ({', '.join([c.name for c in Color])}): ").strip().upper()
            try:
                color_value = Color[color].value
                print("✔️ Tag set:", service.add_tag(doc_oid, tag, color_value))
            except KeyError:
                print("❌ Invalid color.")
        elif action == "untag":
            print("✔️ Tag removed:", service.remove_tag(doc_oid))
        elif action == "showtag":
            tag_obj = service.get_document_tag(doc_oid)
            print(f"📎 {tag_obj.name}, {tag_obj.color}" if tag_obj else "No tag.")
        elif action == "bibtex":
            buffer, name = service.download_bibtex(doc_oid)
            if buffer:
                with open(name, "wb") as f:
                    f.write(buffer.getvalue())
                print(f"📥 BibTeX downloaded as {name}")
            else:
                print("❌ No BibTeX available.")
        elif action == "delete":
            confirm = input("⚠️ Confirm deletion (yes)? ").lower()
            if confirm == "yes":
                print("✔️ Deleted:", service.delete_document(doc_oid))
            else:
                print("❎ Canceled.")
        else:
            print("❌ Invalid action.")
