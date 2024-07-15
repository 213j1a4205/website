from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS links (id INTEGER PRIMARY KEY, url TEXT)')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_link', methods=['POST'])
def add_link():
    url = request.json['url']
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO links (url) VALUES (?)', (url,))
        conn.commit()
    return jsonify({"message": "Link added successfully"}), 201

@app.route('/get_links', methods=['GET'])
def get_links():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT url FROM links')
        links = cursor.fetchall()
    return jsonify([link[0] for link in links])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
