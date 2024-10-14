import os
from os.path import dirname, join

from bson.objectid import ObjectId
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
from werkzeug.utils import secure_filename

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Koneksi ke MongoDB
MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")
conn = MongoClient(MONGODB_URI)
db = conn[DB_NAME]

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    books = list(db.book_api.find({}))
    return render_template("index.html", books=books)

@app.route("/books", methods=["GET"])
def book():
    books = list(db.book_api.find({}))
    return render_template("books.html", books=books)

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")

# API untuk menambah buku
@app.route("/books/add", methods=["POST"])
def add_book():
    title = request.form["title_give"]
    author = request.form["author_give"]
    year = request.form["year_give"]
    genre = request.form["genre_give"]
    price = request.form["price_give"]

    # Mengambil file foto dari request
    photo = request.files["photo_give"]
    filename = secure_filename(photo.filename)
    extension = filename.split(".")[-1]
    file_path = f"static/cover_buku/{title.replace(' ', '_')}.{extension}"
    photo.save(file_path)

    # Menyimpan informasi buku ke database (MongoDB)
    book_data = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "price": price,
        "photo": file_path,  
    }
    db.book_api.insert_one(book_data)

    return jsonify({"message": "Book added successfully"})

# API untuk menghapus buku
@app.route("/books/delete", methods=["POST"])
def delete_book():
    title = request.form["title_give"]
    db.book_api.delete_one({"title": title})  
    return jsonify({"message": "Book deleted successfully"})

# API untuk mengedit buku
@app.route("/books/edit", methods=["POST"])
def edit_book():
    book_id = request.form["id_give"]  
    new_data = {
        "title": request.form["title_give"],
        "author": request.form["author_give"],
        "year": request.form["year_give"],
        "genre": request.form["genre_give"],
        "price": request.form["price_give"],
    }

    
    db.book_api.update_one({"_id": ObjectId(book_id)}, {"$set": new_data})
    return jsonify({"message": "Book updated successfully"})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
