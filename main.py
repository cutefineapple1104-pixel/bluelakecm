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
