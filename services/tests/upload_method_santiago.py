from database.repository.user_repository import User
from services.document_service import DocumentService
from services.project_service import ProjectService
from services.upload_manager.document_upload_service import get_pdf_sha256
from services.upload_manager.server_conection import download_document, upload_document, delete_remote_directory


user_id_1 = ""
user_id_2 = ""
project_id_1 = ""
project_id_2 = ""

def create_two_users():
    # create users in mongo db
    user_data_1 = {
        # Google's unique ID
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe2@example.com",
        "sub_id": "1076915035000615071530",
    }

    user_data_2 = {

        "first_name": "Maria",
        "last_name": "perez",
        "email": "maria.perez@example.com",
        "sub_id": "1076915035000615071531",  # Google's unique ID
    }

    user_1 = User(
        first_name=user_data_1["first_name"],
        last_name=user_data_1["last_name"],
        email=user_data_1["email"],
        sub_id=user_data_1["sub_id"]
    )

    user_2 = User(
        first_name=user_data_2["first_name"],
        last_name=user_data_2["last_name"],
        email=user_data_2["email"],
        sub_id=user_data_2["sub_id"]
    )

    try:
        global user_id_1
        user_id_1= user_1.new_user()
        print(f"Successfully created user: {user_data_1['email']}")
        global user_id_2
        user_id_2 = user_2.new_user()
        print(f"Successfully created user: {user_data_2['email']}")
    except Exception as e:
        print(f"Error creating user: {str(e)}")

project_id_1_1 = ""
project_id_1_2 = ""
project_id_2_1 = ""
project_id_2_2 = ""

path_1 = r"C:\Users\User\PycharmProjects\arcai\papers\Automatic_Visual_Detection_of_Fresh_Poultry_Egg_Quality_Inspection_using_Image_Processing.pdf"
path_2 = r"C:\Users\User\PycharmProjects\arcai\papers\Blending_Immersive_Gameplay_with_Intense_Exercise_Using_Asynchronous_Exergaming.pdf"
path_3 = r"C:\Users\User\PycharmProjects\arcai\papers\Efficient_Embedding_of_Scale-Free_Graphs_in_the_Hyperbolic_Plane.pdf"
path_4 = r"C:\Users\User\PycharmProjects\arcai\papers\Online_level_generation_in_Super_Mario_Bros_via_learning_constructive_primitives.pdf"

rel_path = "user_1/project_1"

def create_projects():
    global project_id_1_1, project_id_1_2, project_id_2_1, project_id_2_2
    #create projects for the user above in mongo db

    project_id_1_1 = ProjectService().create_project(user_id_1, "project_1_1").to_dict().get("_id")
    project_id_1_2 = ProjectService().create_project(user_id_1, "project_1_2").to_dict().get("_id")

    project_id_2_1 = ProjectService().create_project(user_id_2, "project_2_1").to_dict().get("_id")
    project_id_2_2 = ProjectService().create_project(user_id_2, "project_2_2").to_dict().get("_id")

def upload_documents_to_created_users():
    #DocumentService().upload_document(path_1, "user_id_1", "project_id_1_1")
    DocumentService().upload_document(path_1, user_id_1, project_id_1_1)
    DocumentService().upload_document(path_2, user_id_1, project_id_1_1)
    DocumentService().upload_document(path_3, user_id_1, project_id_1_1)

    DocumentService().upload_document(path_1, user_id_1, project_id_1_2)
    DocumentService().upload_document(path_2, user_id_1, project_id_1_2)
    DocumentService().upload_document(path_3, user_id_1, project_id_1_2)




def method_upload_document_TEST():
    #this test the direct method to the server not in mongo
    upload_document(path_1, rel_path, get_pdf_sha256(path_1))
    upload_document(path_2, rel_path, get_pdf_sha256(path_2))
    upload_document(path_3, rel_path, get_pdf_sha256(path_3))
    upload_document(path_4, rel_path, get_pdf_sha256(path_4))

def method_download_document_TEST():
    download_document(
        r"/home/pse03/user_1/project_1/3b00398ebdc88c0975005cabd8b193c52c58daffd2625d3a0964f107725d87c2/3b00398ebdc88c0975005cabd8b193c52c58daffd2625d3a0964f107725d87c2.pdf",
        r"C:\Users\User\Desktop\testArcAi",
        "paper_1")
    download_document(
        r"/home/pse03/user_1/project_1/b04ab48891f0e905ac304e21ffa503841c3f7fac295d417ba069e873c72db80e/b04ab48891f0e905ac304e21ffa503841c3f7fac295d417ba069e873c72db80e.pdf",
        r"C:\Users\User\Desktop\testArcAi",
        "paper_2")
    download_document(
        r"/home/pse03/user_1/project_1/6fdd936612ea3210f5bbbd2ad98ececed412400a2dd84d562b992258fbe9f417/6fdd936612ea3210f5bbbd2ad98ececed412400a2dd84d562b992258fbe9f417.pdf",
        r"C:\Users\User\Desktop\testArcAi",
        "paper_3")
    download_document(
        r"/home/pse03/user_1/project_1/898b29a276747664ddb4b2c9aece69e117eb475d76a5fb63fbdf8bbfd4a76faf/898b29a276747664ddb4b2c9aece69e117eb475d76a5fb63fbdf8bbfd4a76faf.pdf",
        r"C:\Users\User\Desktop\testArcAi",
        "paper_4")

def method_delete_remote_directory_TEST():
    delete_remote_directory(
        r"/home/pse03/user_1/project_1/3b00398ebdc88c0975005cabd8b193c52c58daffd2625d3a0964f107725d87c2/3b00398ebdc88c0975005cabd8b193c52c58daffd2625d3a0964f107725d87c2.pdf")
    delete_remote_directory(
        r"/home/pse03/user_1/project_1/b04ab48891f0e905ac304e21ffa503841c3f7fac295d417ba069e873c72db80e/b04ab48891f0e905ac304e21ffa503841c3f7fac295d417ba069e873c72db80e.pdf")
    delete_remote_directory(
        r"/home/pse03/user_1/project_1/6fdd936612ea3210f5bbbd2ad98ececed412400a2dd84d562b992258fbe9f417/6fdd936612ea3210f5bbbd2ad98ececed412400a2dd84d562b992258fbe9f417.pdf")
    delete_remote_directory(
        r"/home/pse03/user_1/project_1/898b29a276747664ddb4b2c9aece69e117eb475d76a5fb63fbdf8bbfd4a76faf/898b29a276747664ddb4b2c9aece69e117eb475d76a5fb63fbdf8bbfd4a76faf.pdf")

if __name__ == "__main__":
    #method_upload_document_TEST()
    #method_download_document_TEST()
    #method_delete_remote_directory_TEST()



    create_two_users()
    create_projects()
    upload_documents_to_created_users()


