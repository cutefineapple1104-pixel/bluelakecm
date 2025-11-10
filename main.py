streamlit
pandas
openpxl
photo_site/
│
├─ app.py
├─ static/
│   └─ uploads/
│
└─ templates/
    ├─ index.html
    ├─ upload.html
    └─ photo.html
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

DB_NAME = 'photos.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            text TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, filename FROM photos ORDER BY id DESC')
    photos = c.fetchall()
    conn.close()
    return render_template('index.html', photos=photos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['photo']
        text = request.form['text']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('INSERT INTO photos (filename, text, created_at) VALUES (?, ?, ?)',
                      (filename, text, datetime.now().isoformat()))
            conn.commit()
            conn.close()

            return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/photo/<int:photo_id>')
def photo(photo_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT filename, text, created_at FROM photos WHERE id=?', (photo_id,))
    photo = c.fetchone()
    conn.close()
    return render_template('photo.html', photo=photo)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>사진 갤러리</title>
<style>
body { font-family: sans-serif; text-align: center; background: #fafafa; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; padding: 20px; }
.grid img { width: 100%; border-radius: 10px; cursor: pointer; transition: 0.3s; }
.grid img:hover { transform: scale(1.03); }
.upload-btn { margin: 20px; display: inline-block; padding: 10px 20px; background: #007bff; color: #fff; border-radius: 8px; text-decoration: none; }
</style>
</head>
<body>
<h1>📸 사진 갤러리</h1>
<a href="/upload" class="upload-btn">새 사진 올리기</a>
<div class="grid">
{% for id, filename in photos %}
  <a href="{{ url_for('photo', photo_id=id) }}">
    <img src="{{ url_for('static', filename='uploads/' + filename) }}" alt="photo">
  </a>
{% endfor %}
</div>
</body>
</html>
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>사진 업로드</title>
<style>
body { font-family: sans-serif; text-align: center; margin-top: 50px; }
form { display: inline-block; padding: 20px; border: 1px solid #ccc; border-radius: 10px; }
textarea { width: 300px; height: 80px; margin-top: 10px; }
button { margin-top: 15px; padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 8px; cursor: pointer; }
button:hover { background: #0056b3; }
</style>
</head>
<body>
<h1>🖼 사진 올리기</h1>
<form method="POST" enctype="multipart/form-data">
    <input type="file" name="photo" accept="image/*" required><br>
    <textarea name="text" placeholder="짧은 글을 써주세요..." required></textarea><br>
    <button type="submit">업로드</button>
</form><br><br>
<a href="/">← 돌아가기</a>
</body>
</html>
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>사진 보기</title>
<style>
body { font-family: sans-serif; text-align: center; background: #f0f0f0; padding-top: 30px; }
img { max-width: 80%; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.2); }
.text-box { margin-top: 20px; font-size: 1.1em; background: #fff; display: inline-block; padding: 15px; border-radius: 8px; width: 60%; }
a { display: block; margin-top: 30px; color: #007bff; text-decoration: none; }
a:hover { text-decoration: underline; }
</style>
</head>
<body>
<img src="{{ url_for('static', filename='uploads/' + photo[0]) }}" alt="photo">
<div class="text-box">{{ photo[1] }}</div>
<a href="/">← 갤러리로 돌아가기</a>
</body>
</html>
