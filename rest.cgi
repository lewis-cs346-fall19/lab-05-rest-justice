#! /usr/bin/python3
def getValue(form, string):
	#gets values from cgi.FieldStorage()
	if string in form:
		return form[string].value
	else:
		return ""
import os
import json
import cgi
import MySQLdb
import passwords
if "PATH_INFO" in os.environ:
	path = os.environ["PATH_INFO"]
	if path=="/rest":
		#hardcoded "magic word"
		print("Content-Type: text/html")
		print("Status: 200 OK")
		print()
		print("<html><head><title>GAME!</title></head><body>")
		print("<b>Jigglypuff Wins!</b>")
		print("</body></html>")
	elif path=="/json":
		#hardcoded json object handling
		print("Content-Type: application/json")
		print("Status: 200 OK")
		print()
		x = ["P","I","K","A","C","H","O","O", {"foo": "asdfjkl;"}]
		x_json = json.dumps(x, indent=2)
		print(x_json)
	elif path.startswith("/courses"):
		#MySQL table GETing and POSTing
		if "REQUEST_METHOD" in os.environ and os.environ["REQUEST_METHOD"]=="POST":
			form = cgi.FieldStorage()
			code = getValue(form, "code")
			credits = getValue(form, "credits")
			title = getValue(form, "title")
			conn = MySQLdb.connect(host=passwords.SQL_HOST,user=passwords.SQL_USER,passwd=passwords.SQL_PASSWORD,db="labDB")
			cursor=conn.cursor()
			cursor.execute('INSERT INTO courses(code,title,credits) VALUES(%s,%s,%s);', (code,title,credits))
			new_id = cursor.lastrowid
			cursor.close()
			conn.commit()
			print("Content-Type: text/html")
			print("Status: 302 Redirect")
			print("Location: /cgi-bin/rest.cgi/courses/" + str(new_id))
			print()
		elif ("REQUEST_METHOD" in os.environ and os.environ["REQUEST_METHOD"]=="GET"):
			id = getValue(cgi.FieldStorage(),"id")
			if id!="":
				print("Content-Type: text/html")
				print("Status: 302 Redirect")
				print("Location: /cgi-bin/rest.cgi/courses/" + id)
				print()
			else:
				conn = MySQLdb.connect(host=passwords.SQL_HOST,user=passwords.SQL_USER,passwd=passwords.SQL_PASSWORD,db="labDB")
				cursor=conn.cursor()
				if (path=="/courses" or path=="/courses/"):
					cursor.execute("SELECT * FROM courses;")
				else:
					id = path[9:len(path)]
					cursor.execute("SELECT * FROM courses WHERE id=%s;", (id,))
				results=cursor.fetchall()
				cursor.close()
				print("Content-Type: application/json")
				print("Status: 200 OK")
				print()
				results_json = json.dumps(results, indent=2)
				print(results_json)
	elif path=="/course_form":
		#debugging html form to construct GET and POST ops on courses table
		print("Content-Type: text/html")
		print("Status: 200 OK")
		print()
		print("""<html><body><p>Add new course<br>
			<form action="/cgi-bin/rest.cgi/courses" method="POST">
			Course Code<input type=number name="code"><br>
			Title<input type=text name="title"><br>
			Credit Amount<input type=number name="credits"><br>
			<input type=submit value="Add Course">
			</form><br><p>Search for ID<br><form action="/cgi-bin/rest.cgi/courses" method="GET">
			<input type=number name="id"><br>
			<input type=submit></form>
			</body></html>""")
	else:
		#default
		print("Content-Type: text/html")
		print("Status: 200 OK")
		print()
		print("<html><head><title>Page</title></head><body>")
		print("<p>path = " + path)
		print("</body></html>")
else:
	print("Content-Type: text/html")
	print("Status: 302 Redirect")
	print("Location: rest.cgi/")
	print()
