from database.repository.user_repository import User
from services.document_service import DocumentService
from services.upload_manager.document_upload_service import get_pdf_sha256
from services.upload_manager.server_conection import download_document, upload_document, delete_remote_directory

"""
1. create some users
2. create some documents

"""


def create_two_users():
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
        user_1.new_user()
        print(f"Successfully created user: {user_data_1['email']}")
        user_2.new_user()
        print(f"Successfully created user: {user_data_2['email']}")
    except Exception as e:
        print(f"Error creating user: {str(e)}")

def create_projects():

    pass
path_1 = r"C:\Users\User\PycharmProjects\arcai\papers\Automatic_Visual_Detection_of_Fresh_Poultry_Egg_Quality_Inspection_using_Image_Processing.pdf"
path_2 = r"C:\Users\User\PycharmProjects\arcai\papers\Blending_Immersive_Gameplay_with_Intense_Exercise_Using_Asynchronous_Exergaming.pdf"
path_3 = r"C:\Users\User\PycharmProjects\arcai\papers\Efficient_Embedding_of_Scale-Free_Graphs_in_the_Hyperbolic_Plane.pdf"
path_4 = r"C:\Users\User\PycharmProjects\arcai\papers\Online_level_generation_in_Super_Mario_Bros_via_learning_constructive_primitives.pdf"

rel_path = "user_1/project_1"


def upload_docs():
    DocumentService.upload_document(path_1, user_id="1076915035000615071530", project_id="project_1")


if __name__ == "__main__":
    #create_two_users()
    #upload_docs()

    #download_document(r"/home/pse03/user_3/project_1/e9f590b807ce6db83d7f266a1198ec883f96506348b8b6790076eb4784b28133.xlsx", r"C:\Users\User\Documents", "kit_manager")
    #DocumentService().download_document("68705790bb6a40dd34395f97", r"C:\Users\User\Desktop\testArcAi")

    #upload_document(path_1, rel_path, get_pdf_sha256(path_1))
    #upload_document(path_2, rel_path, get_pdf_sha256(path_2))
    #upload_document(path_3, rel_path, get_pdf_sha256(path_3))
    #upload_document(path_4, rel_path, get_pdf_sha256(path_4))

    download_document(r"/home/pse03/user_1/project_1/3b00398ebdc88c0975005cabd8b193c52c58daffd2625d3a0964f107725d87c2/3b00398ebdc88c0975005cabd8b193c52c58daffd2625d3a0964f107725d87c2.pdf",
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

    delete_remote_directory(r"/home/pse03/user_1/project_1/3b00398ebdc88c0975005cabd8b193c52c58daffd2625d3a0964f107725d87c2")