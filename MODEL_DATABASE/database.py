
from config import cursor, mydb

#Strings for database
STRING_DB_NAME = "fullstack"
STRING_SHOW_DATABASES = "show databases"
STRING_USE_DATABASE = "use {}"
STRING_CREATE_DATABASE = "create database {}"

#Strings for Tables
STRING_SHOW_TABLES = "show tables"
STRING_CREATE_TABLE = "create table {} ({})"
STRING_CREATE_TABLE_AUTO_INCREMENT = "create table {} ({})AUTO_INCREMENT = 1"
STRING_SELECT_TABLE_WHOLE = "select * from {}"
STRING_DESCRIBE_TABLE = "describe {}"

# Strings to create the Users table
STRING_USERS_TABLE_NAME = "USERS"
STRING_USERS_COLUMN = ("Sub VARCHAR(255) PRIMARY KEY, "
                       "Name VARCHAR(80) NOT NULL UNIQUE, "
                       "Email VARCHAR(100) NOT NULL UNIQUE, "
                       "CHECK (Email LIKE '_%@_%._%')")
STRING_INSERT_ROW_USERS = "insert into USERS(Sub, Name, Email) value ('"'{}'"', '"'{}'"', '"'{}'"')"
STRING_USER_PRESENT_CHECK = "select * from users where Sub = '"'{}'"'"

# Strings to create the Libraries table
STRING_LIBRARIES_TABLE_NAME = "LIBRARIES"
STRING_LIBRARIES_COLUMN = ("Library_ID int Primary key auto_increment, "
                           "Sub varchar(255) unique NOT NULL, "
                           "Foreign key (Sub) references Users(Sub) On delete cascade")
STRING_INSERT_ROW_LIBRARIES = "insert into LIBRARIES(Sub) value ('"'{}'"')"
STRING_GET_LIBRARY_ID = "select * from LIBRARIES where Sub = '"'{}'"'"

#Strings to create the Projects table
STRING_PROJECTS_TABLE_NAME = "PROJECTS"
STRING_PROJECTS_COLUMN = ("Project_ID int auto_increment,"
                          "Library_ID int NOT NULL, "
                          "Parent_Project_ID int default NULL,"
                          "Name varchar(80) NOT NULL UNIQUE,"
                          "Created_At timestamp default current_timestamp,"
                          "foreign key (Library_ID) references Libraries(Library_ID) On delete cascade,"
                          "foreign key (Parent_Project_ID) references Projects(Project_ID) On delete cascade,"
                          "Primary key(Project_ID, Library_ID)")
STRING_GET_ALL_PROJECTS_FROM_USER = "select * from PROJECTS where Library_ID = '"'{}'"'"
STRING_INSERT_ROW_PROJECTS = "insert into PROJECTS(Library_ID, Name) value ({}, '"'{}'"')"
STRING_INSERT_ROW_PROJECTS_FOLDER = "insert into PROJECTS(Parent_Project_ID, Library_ID, Name) value ({}, {}, '"'{}'"')"

#Strings to create the Documents table
STRING_DOCUMENTS_TABLE_NAME = "DOCUMENTS"
STRING_DOCUMENTS_COLUMN = ("Document_ID int auto_increment,"
                           "Project_ID int NOT NULL,"
                           "Library_ID int NOT NULL,"
                           "Name varchar(80) NOT NULL,"
                           "File_Path varchar(255) NOT NULL,"
                           "Uploaded_At timestamp DEFAULT CURRENT_TIMESTAMP,"
                           "File_Data LONGTEXT NOT NULL,"
                           "foreign key (Project_ID) references Projects(Project_ID) ON DELETE CASCADE,"
                           "foreign key (Library_ID) references Libraries(Library_ID) On delete cascade,"
                           "Primary key(Document_ID, Library_ID)")
STRING_INSERT_ROW_DOCUMENTS = "insert into DOCUMENTS(Project_ID, Name, File_Path, File_Data) value({},'"'{}'"', '"'{}'"', '"'{}'"')"


def show_database():
    cursor.execute(STRING_SHOW_DATABASES)
    return cursor.fetchall()


def db_present(database_name):
    database_list = show_database()
    for database in database_list:
        if database[0] == database_name.lower():
            return True
    return False


def use_database(db_name):
    cursor.execute(STRING_USE_DATABASE.format(db_name))


def show_tables():
    cursor.execute(STRING_SHOW_TABLES)
    return cursor.fetchall()


def create_database(db_name):
    if not db_present(db_name):
        cursor.execute(STRING_CREATE_DATABASE.format(db_name))
        mydb.commit()
        print("Database has been created")
    else:
        print(f"Database {db_name} already exists")

def create_table(table_name, columns):
    if not table_present(table_name):
        cursor.execute(STRING_CREATE_TABLE.format(table_name, columns))
        mydb.commit()
        print("Table has been created")
    else:
        print(f"Table {table_name} already exists")

def create_table_with_auto_increment(table_name, columns):
    if not table_present(table_name):
        cursor.execute(STRING_CREATE_TABLE_AUTO_INCREMENT.format(table_name, columns))
        mydb.commit()
        print("Table has been created")
    else:
        print(f"Table {table_name} already exists")


def select_table(table_name):
    cursor.execute(STRING_SELECT_TABLE_WHOLE.format(table_name))


def describe_table(table_name):
    cursor.execute(STRING_DESCRIBE_TABLE.format(table_name))
    for x in cursor:
        print(x)

def insert_row_in_table_users(sub, name, email):
    try:
        print(STRING_INSERT_ROW_USERS.format(sub, name, email))
        cursor.execute(STRING_INSERT_ROW_USERS.format(sub, name, email))
        mydb.commit()
    except Exception as e:
        print(e)

def insert_row_in_table_libraries(email):
    try:
        cursor.execute(STRING_INSERT_ROW_LIBRARIES.format(email))
        mydb.commit()
    except Exception as e:
        print(e)

def insert_row_in_table_projects(library_id, parent_project_id, name):
    try:
        if parent_project_id is None:
            print(STRING_INSERT_ROW_PROJECTS.format(library_id, name))
            cursor.execute(STRING_INSERT_ROW_PROJECTS.format(library_id, name))
            mydb.commit()
        else:
            print(STRING_INSERT_ROW_PROJECTS_FOLDER.format(library_id, parent_project_id, name))
            cursor.execute(STRING_INSERT_ROW_PROJECTS_FOLDER.format(library_id, parent_project_id, name))
            mydb.commit()
    except Exception as e:
        print(e)

def insert_row_in_table_documents(project_id, name, file_path, file_data):
    try:
        print(STRING_INSERT_ROW_DOCUMENTS.format(project_id, name, file_path, file_data))
        cursor.execute(STRING_INSERT_ROW_DOCUMENTS.format(project_id, name, file_path, file_data))
        mydb.commit()
    except Exception as e:
        print(e)

def table_present(table_name):
    tables_list = show_tables()
    for table in tables_list:
        if table[0] == table_name.lower():
            return True
    return False

def create_all_required_tables():
    create_table(STRING_USERS_TABLE_NAME, STRING_USERS_COLUMN)
    create_table_with_auto_increment(STRING_LIBRARIES_TABLE_NAME, STRING_LIBRARIES_COLUMN)
    create_table_with_auto_increment(STRING_PROJECTS_TABLE_NAME, STRING_PROJECTS_COLUMN)
    create_table_with_auto_increment(STRING_DOCUMENTS_TABLE_NAME, STRING_DOCUMENTS_COLUMN)

def user_exists(sub):
    cursor.execute(STRING_USER_PRESENT_CHECK.format(sub))
    if cursor.fetchone() is None:
        return False
    return True

# Creates all the databases required for our application to run
def database_setup():
    create_database(STRING_DB_NAME)
    use_database(STRING_DB_NAME)
    create_all_required_tables()

# Gives the library id of the user
def get_library_id(sub):
    print(STRING_GET_LIBRARY_ID.format(sub))
    cursor.execute(STRING_GET_LIBRARY_ID.format(sub))
    library_list = cursor.fetchall()
    print(library_list)
    if len(library_list) == 0:
        return None
    library_id = library_list[0][0]
    return library_id

# Gives the number of projects of a particular user
def number_of_projects(sub):
    cursor.execute(STRING_GET_ALL_PROJECTS_FROM_USER.format(get_library_id(sub)))
    all_projects = cursor.fetchall()
    return len(all_projects)

# Gives the number of projects of a particular user
def project_list(sub):
    cursor.execute(STRING_GET_ALL_PROJECTS_FROM_USER.format(get_library_id(sub)))
    all_projects = cursor.fetchall()
    print(all_projects)
    return all_projects

use_database(STRING_DB_NAME)
project_list("117530366620837166459")











