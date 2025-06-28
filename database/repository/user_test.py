from database.repository.project_repository import Project
from database.repository.user_repository import User



def create_sample_user():
    # Sample user data
    user_data = {
        "sub_id": "1076915035000615071530",  # Google's unique ID
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe2@example.com"
    }

    # Create User instance
    user = User(
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        email=user_data["email"],
        sub_id=user_data["sub_id"]
    )

    # Call the method
    try:
        user.new_user()
        print(f"Successfully created user: {user_data['email']}")
    except Exception as e:
        print(f"Error creating user: {str(e)}")

def create_sample_project():
    # Sample user data
    project_data = {
        "user_id": "1076915035000615071530",  # Google's unique ID
        "project_name": "John",
        "nate": "Hola todas las perras hahahah",
    }

    # Create User instance
    project = Project(
        user_id = project_data["user_id"],
        project_name = project_data["project_name"],
        note = project_data["nate"]
    )

    # Call the method
    try:
        project.new_project()
        print(f"Successfully project user: {project_data['project_name']}")
    except Exception as e:
        print(f"Error creating project !!!!: {str(e)}")





if __name__ == "__main__":
    create_sample_user()



    User.get_all_users()
    #print(User.update_user_name("10769150350006150715113082367", "manuel"))
    print("#######################################")
    print(type(User.get_user_by_id("10769150350006150715113082367")))

    ##project
    print("##########PROJECT#############################")
    create_sample_project()
    print(Project.get_project_by_user_id("1076915035000615071530"))
