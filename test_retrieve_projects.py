from services.project_service import ProjectService
from services.library_service import LibraryService

if __name__ == "__main__":
    print("=== Manual Integration Test: Project Sorting ===")
    service = ProjectService()
    library_service = LibraryService()

    # 1) Ask for user ID
    user_id = int(input("Enter user_id to retrieve projects: ").strip())

    # 2) Fetch all projects
    projects = service.get_user_projects(user_id)
    if not projects:
        print("\n❌ No projects found for that user_id!")
        exit(1)

    # 3) Print initially
    print(f"\nFound {len(projects)} projects for user_id={user_id} (unsorted):")
    for i, proj in enumerate(projects, start=1):
        print(f"Project {i}: id={proj.id}, name={proj.project_name}, user_id={proj.user_id}")

    # 4) Menu loop
    while True:
        print("\n=== Sorting Menu ===")
        print("1) Sort by name (asc)")
        print("2) Sort by name (desc)")
        print("3) Sort by created_at (asc)")
        print("4) Sort by created_at (desc)")
        print("5) Sort by updated_at (asc)")
        print("6) Sort by updated_at (desc)")
        print("0) Exit")

        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Exiting.")
            break
        elif choice == "1":
            sorted_projects = library_service.sort_library(user_id, sort_by="name", order="asc")
        elif choice == "2":
            sorted_projects = library_service.sort_library(user_id, sort_by="name", order="desc")
        elif choice == "3":
            sorted_projects = library_service.sort_library(user_id, sort_by="created", order="asc")
        elif choice == "4":
            sorted_projects = library_service.sort_library(user_id, sort_by="created", order="desc")
        elif choice == "5":
            sorted_projects = library_service.sort_library(user_id, sort_by="updated", order="asc")
        elif choice == "6":
            sorted_projects = library_service.sort_library(user_id, sort_by="updated", order="desc")
        else:
            print("❌ Invalid choice. Try again.")
            continue

        print(f"\nSorted Projects ({choice}):")
        for i, proj in enumerate(sorted_projects, start=1):
            print(f"Project {i}: id={proj.id}, name={proj.project_name}, user_id={proj.user_id}, "
                f"created_at={proj.created_at}, updated_at={proj.updated_at}")
