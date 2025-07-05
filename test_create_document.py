from services.document_service import DocumentService
from bson import ObjectId

if __name__ == "__main__":
    print("=== Manual Integration Test: DocumentService.create_document ===")

    service = DocumentService()

    # Replace with a valid existing project ID in your DB:
    project_id = input("Enter project_id to attach document to: ").strip()

    # 1) Create a new document with dummy data
    created_doc = service.create_document(
        name="MyTestDoc",
        project_id=project_id,
        path="/fake/path/to/doc.pdf",
        vector_store_path="/fake/path/to/vector.store",
        author="John Doe",
        year="2025",
        journal="Test Journal",
        pages=10,
        bibtex="@article{doe2025, title={My Test}, author={John Doe}}",
    )
    print("\n✅ Document creation attempted! Go check Compass: database 'arcai' -> collection 'documents'.")

    # 2) Optionally: Prompt to retrieve document immediately
    choice = input("\nWould you like to fetch all documents in this project now? (y/n): ").strip().lower()
    if choice == "y":
        docs = service.get_project_documents(project_id)
        if docs:
            print(f"\nFound {len(docs)} documents in project {project_id}:")
            for i, doc in enumerate(docs, start=1):
                print(f"Document {i}: id={doc.id}, name={doc.name}, author={doc.author}, year={doc.year}")
        else:
            print("\n❌ No documents found for that project.")
