import sqlite3

with sqlite3.connect('sample.db') as conn:
	cursor = conn.cursor()
	cursor.execute("DROP TABLE posts")
	cursor.execute("CREATE TABLE posts(title TEXT,description TEXT);")
	#c.execute('INSERT INTO posts VALUES(request.form['title'],request.form['text'])')
	#c.execute('INSERT INTO posts VALUES("well","tight")')