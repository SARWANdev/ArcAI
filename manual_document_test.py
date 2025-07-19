import os
from bson import ObjectId
from services.document_service import DocumentService
from services.project_service import ProjectService
from model.document_reader.tag_manager.color import Color
from services.notebook_service import NotebookService

def prompt_sort_criteria():
    fields = ["title", "first_author", "year", "journal", "created_at"]
    print("\nAvailable fields:")
    for field in fields:
        print(f"• {field}")

    print("\nYou can only sort by ONE field at a time.")
    print("Use the format: field:asc or field:desc")
    print("Example: title:asc\n")

    user_input = input("Enter sort field: ").strip()
    if not user_input:
        return None

    parts = user_input.split(":")
    if len(parts) != 2 or parts[0] not in fields or parts[1] not in ["asc", "desc"]:
        print(f"⚠️ Invalid input: {user_input}")
        return None

    return (parts[0], parts[1])

def prompt_filter_criteria():
    print("\nFilter Options:")
    read_str = input("Filter by read status? (yes/no/skip): ").strip().lower()
    favorite_str = input("Filter by favorite status? (yes/no/skip): ").strip().lower()
    tag = input("Filter by tag (exact match)? Leave blank to skip: ").strip()

    def parse_bool(val):
        return True if val == "yes" else False if val == "no" else None

    read = parse_bool(read_str)
    favorite = parse_bool(favorite_str)
    return read, favorite, tag if tag else None

if __name__ == "__main__":
    document_service = DocumentService()
    project_service = ProjectService()
    notebook_service = NotebookService()

    pdf_path = input("Enter full path to PDF file: ").strip()
    user_id = input("Enter user_id (Google sub): ").strip()
    project_id = input("Enter project_id: ").strip()

    print("\nUploading document...")
    document_service.upload_document(
        document_path=pdf_path,
        user_id=user_id,
        project_id=project_id,
        original_name= os.path.basename(pdf_path),
    )
    print("✔️ Upload complete.\n")

    current_sort = []
    current_filter = None  # Tuple: (read, fav, tag)

    while True:
        if current_sort and current_filter:
            read, favorite, tag = current_filter
            docs = document_service.get_filtered_and_sorted_documents(
                project_id,
                current_sort[0], current_sort[1],
                read=read,
                favorite=favorite,
                tag=tag
            )
        elif current_filter:
            read, favorite, tag = current_filter
            docs = document_service.filter_documents(project_id, read=read, favorite=favorite, tag=tag)
        elif current_sort:
            docs = project_service.sort_project_documents(project_id, current_sort[0], current_sort[1])
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
        print("Type 'filter' to apply filter")
        print("Type 'sort+filter' to set both at once")

        user_input = input("Select document (number) or action: ").strip().lower()

        if user_input == "0":
            break
        elif user_input == "sort":
            current_sort = prompt_sort_criteria()
            current_filter = None  # clear filter when sorting
            continue
        elif user_input == "filter":
            current_filter = prompt_filter_criteria()
            current_sort = []  # clear sort when filtering
            continue
        elif user_input == "sort+filter":
            current_sort = prompt_sort_criteria()
            current_filter = prompt_filter_criteria()
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
            "\nChoose action: read | unread | fav | unfav | tag | untag | showtag | bibtex | delete | show note | update note\n> "
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
        elif action == "shownote":
            note = notebook_service.get_documents_notebook(doc_oid)
            print(f"📝 Note:\n{note}" if note else "📭 No note found.")

        elif action == "updatenote":
            print("Enter new note content (leave empty to cancel):")
            new_note = input("Note:\n")
            if new_note.strip() == "":
                print("❎ Update canceled.")
            else:
                success = notebook_service.update_document_notebook(doc_oid, new_note)
                print("✔️ Note updated." if success else "❌ Failed to update note.")
        else:
            print("❌ Invalid action.")
