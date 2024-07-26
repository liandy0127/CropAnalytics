print("Initializing Flask app")
from flask import Flask
import psycopg2

# Initialize Flask application
app = Flask(__name__)

# Function to create a database connection
def get_db_conn():
    conn = psycopg2.connect(
        dbname="crops",
        user="postgres",
        password="160320",
        host="localhost",
        port="5432"
    )
    return conn

# Import routes after app initialization to avoid circular import issues
print("Importing routes")
from app import routes
