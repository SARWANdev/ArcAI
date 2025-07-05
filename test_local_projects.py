import time
from services.project_service import ProjectService
from bson import ObjectId

if __name__ == "__main__":
    print("=== Manual Integration Test: ProjectService.create_project + rename_project ===")

    service = ProjectService()

    # 1) Create a project using the service
    created_proj = service.create_project(user_id=6666, project_name="SP")
    print(f"\nCreated Project: id={created_proj.id}, name={created_proj.project_name}, user_id={created_proj.user_id}")

    # 2) Fetch the created project by ID (using service.get_project)
    fetched_proj = service.get_project(created_proj.id)
    print(f"\nFetched Project Before Rename: {vars(fetched_proj) if fetched_proj else None}")

    # 3) Wait a bit so updated_at timestamp will visibly change
    print("\nSleeping for 5 seconds to see updated_at difference...")
    time.sleep(5)

    # 4) Rename the project using the service.rename_project
    if fetched_proj:
        rename_result = service.rename_project(ObjectId(str(fetched_proj.id)), "ItsNotSP")
        print(f"\nRename Result: {rename_result}")

        # 5) Fetch the project again after renaming
        updated_proj = service.get_project(ObjectId(str(created_proj.id)))
        print(f"\nFetched Project After Rename: {vars(updated_proj) if updated_proj else None}")
    else:
        print("\n❌ Project not found for renaming!")

    print("\n✅ Check Compass: database 'arcai' -> collection 'projects'")
