from flask import Flask, request, redirect, send_from_directory
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# MySQL configuration
db_config = {
    'host': 'localhost',
    'user': 'root',         # your MySQL username
    'password': '1234',     # your MySQL password
    'database': 'kkfitness' # your database name
}

# Create users table if it doesn't exist
def init_db():
    # Connect without specifying database to create it if needed
    conn = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password']
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS kkfitness")
    cursor.close()
    conn.close()

    # Now connect to the new database and create the table if needed
    conn = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Call the function to initialize the database and table
init_db()

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        cursor.close()
        conn.close()
        return "Registration successful!"
    except mysql.connector.IntegrityError:
        return "Username already exists."
    except Exception as e:
        return f"Error: {e}"

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return "success"
        else:
            return "fail"
    except Exception as e:
        return "fail"
    
if __name__ == '__main__':
    app.run(debug=True)
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')
