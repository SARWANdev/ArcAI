from services.project_service import ProjectService
from bson import ObjectId

if __name__ == "__main__":
    print("=== Manual Integration Test: ProjectService.delete_project ===")

    service = ProjectService()

    # ➤ Provide an existing project ObjectId (replace with real ID from Compass if needed)
    project_id = input("Enter the ObjectId of the project you want to delete: ").strip()

    if project_id:
        # Delete the project
        deleted = service.delete_project(ObjectId(project_id))
        print(f"\nDelete result: {deleted}")

        # Try fetching it afterwards
        fetched = service.get_project(ObjectId(project_id))
        print(f"\nFetch after delete (should be None): {fetched}")
    else:
        print("❌ No project ID provided!")

    print("\n✅ Done! Check Compass to confirm deletion.")
