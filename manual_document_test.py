import os
from bson import ObjectId
from services.document_service import DocumentService
from services.project_service import ProjectService  # NEW
from model.document_reader.tag_manager.color import Color

def prompt_sort_criteria():
    fields = ["title", "first_author", "year", "journal", "created_at"]
    print("\nAvailable fields:")
    for field in fields:
        print(f"• {field}")

    print("\nYou can specify up to 4 sort fields.")
    print("For each field, use the format: field:asc or field:desc")
    print("Example: title:asc,year:desc\n")

    user_input = input("Enter sort fields (comma-separated): ").strip()
    if not user_input:
        return []

    criteria = []
    for item in user_input.split(","):
        parts = item.strip().split(":")
        if len(parts) != 2 or parts[0] not in fields or parts[1] not in ["asc", "desc"]:
            print(f"⚠️ Invalid input: {item}")
            continue
        criteria.append((parts[0], parts[1]))

    return criteria

if __name__ == "__main__":
    document_service = DocumentService()
    project_service = ProjectService()

    pdf_path = input("Enter full path to PDF file: ").strip()
    user_id = input("Enter user_id (Google sub): ").strip()
    project_id = input("Enter project_id: ").strip()

    print("\nUploading document...")
    document_service.upload_document(
        document_path=pdf_path,
        user_id=user_id,
        project_id=project_id
    )
    print("✔️ Upload complete.\n")

    current_sort = []  # to keep current sort applied

    while True:
        if current_sort:
            docs = project_service.sort_project_documents(project_id, current_sort)
        else:
            docs = document_service.get_project_documents(project_id)

        if not docs:
            print("No documents found.")
            break

        print(f"\n📂 Found {len(docs)} documents in project {project_id}:")
        for i, doc in enumerate(docs, 1):
            print(f"{i}. id={doc.document_id}, name={doc.name}, read={doc.is_read()}, fav={doc.is_favorite()}")

        print("\n0) Quit")
        print("Type 'sort' to change sorting")

        user_input = input("Select document (number) or action: ").strip().lower()

        if user_input == "0":
            break
        elif user_input == "sort":
            current_sort = prompt_sort_criteria()
            continue

        try:
            choice = int(user_input)
        except ValueError:
            print("⚠️ Invalid input. Try again.")
            continue

        if not (1 <= choice <= len(docs)):
            print("⚠️ Out of range. Try again.")
            continue

        selected_doc = docs[choice - 1]
        doc_oid = ObjectId(str(selected_doc.document_id))

        action = input(
            "\nChoose action: read | unread | fav | unfav | tag | untag | showtag | bibtex | delete\n> "
        ).strip().lower()

        if action == "read":
            print("✔️ Marked as read:", document_service.mark_as_read(doc_oid))
        elif action == "unread":
            print("✔️ Marked as unread:", document_service.mark_as_unread(doc_oid))
        elif action == "fav":
            print("✔️ Added to favorites:", document_service.add_to_favorites(doc_oid))
        elif action == "unfav":
            print("✔️ Removed from favorites:", document_service.remove_from_favorites(doc_oid))
        elif action == "tag":
            tag = input("Tag name: ").strip()
            color = input(f"Color ({', '.join([c.name for c in Color])}): ").strip().upper()
            try:
                color_value = Color[color].value
                print("✔️ Tag set:", document_service.add_tag(doc_oid, tag, color_value))
            except KeyError:
                print("❌ Invalid color.")
        elif action == "untag":
            print("✔️ Tag removed:", document_service.remove_tag(doc_oid))
        elif action == "showtag":
            tag_obj = document_service.get_document_tag(doc_oid)
            print(f"📎 {tag_obj.name}, {tag_obj.color}" if tag_obj else "No tag.")
        elif action == "bibtex":
            buffer, name = document_service.download_bibtex(doc_oid)
            if buffer:
                with open(name, "wb") as f:
                    f.write(buffer.getvalue())
                print(f"📥 BibTeX downloaded as {name}")
            else:
                print("❌ No BibTeX available.")
        elif action == "delete":
            confirm = input("⚠️ Confirm deletion (yes)? ").lower()
            if confirm == "yes":
                print("✔️ Deleted:", document_service.delete_document(doc_oid))
            else:
                print("❎ Canceled.")
        else:
            print("❌ Invalid action.")
