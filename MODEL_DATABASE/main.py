from flask import request, jsonify
from config import app
from database import (database_setup, insert_row_in_table_users, user_exists, insert_row_in_table_libraries,
                      insert_row_in_table_projects, number_of_projects, project_list)

logged_in_user = None

# Create a function which gives all the projects of the specific user and let the front end print the list of projects.
@app.route('/logged', methods=['POST'])
def user_info():
    global logged_in_user
    data = request.get_json()
    print("Received data:", data)
    logged_in_user = data['sub']
    if not user_exists(logged_in_user):
        insert_row_in_table_users(logged_in_user, data["name"], data["email"])
        insert_row_in_table_libraries(logged_in_user)
    return jsonify({"status": "success", "message": "Data received", "received": data})
# @app.route('/upload', methods=['POST'])
# def upload():
#     data = request.get_json()
#     print("Received data:", data)
#     insert_row_in_table_files("files", data["name"], data["data"])
#     return jsonify({"status": "success", "message": "Data received", "received": data})

@app.route('/get-projects', methods=['GET'])
def get_projects():
    global logged_in_user
    if not user_exists(logged_in_user):
        return jsonify({"status": "success", "message": "Data received", "received": None})
    list_of_projects = []
    for project in project_list(logged_in_user):
        project_dict = {'Project_ID': project[0], 'Parent_Project_ID': project[2], 'Name': project[3], "Created_At": project[4]}
        list_of_projects.append(project_dict)
    return jsonify({"projects": list_of_projects})


@app.route('/create-project', methods=['POST'])
def add_project():
    global logged_in_user
    insert_row_in_table_projects(logged_in_user, "PROJECT" + str(number_of_projects(logged_in_user) + 1))
    return jsonify({"status": "success", "message": "Data received", "received": "Project created"})

database_setup()
if __name__ == '__main__':
    app.run(debug=True)