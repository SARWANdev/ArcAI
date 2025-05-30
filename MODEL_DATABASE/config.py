from flask import Flask
from flask_cors import CORS
import mysql.connector
# To launch the application for backend
app = Flask(__name__)
CORS(app)  # Allows requests from any origin


# To create a connection between mysql and python
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Chinu@381973",
)
cursor = mydb.cursor()




