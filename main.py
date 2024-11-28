import requests
from flask import Flask,request, render_template
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(

    host= "172.31.3.17",
    user="root",
    password="StrongPass123!",
    database="regrets_db"
)

cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS regrets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text VARCHAR(255) NOT NULL
)
""")


@app.route('/')
def index():
    return '''
        <form method="post" action="/submit">
            <label for="regret">Whats your biggest regret?</label>
            <input type="text" name="regret" id="regret" required>
            <button type="submit">Submit</button>
        </form>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    regret = request.form['regret']
    cursor.execute("INSERT INTO regrets (text) VALUES (%s)", (regret,))
    db.commit()
    return "Thank you for sharing!"

if __name__ == '__main__':
    app.run(debug=True)

