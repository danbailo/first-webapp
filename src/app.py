from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/")
def index():
	return "<a href='/posts'>Posts</a>"

@app.route("/posts")
@app.route("/posts/<int:id_>")
def posts(id_=None):
	title = request.args.get("title")
	data = {
		"path": request.path,
		"referrer": request.referrer,
		"content_type": request.content_type,
		"method": request.method,
		"title": title,
		"id_": id_
	}
	print(data)
	return data	

@app.route("/response")
def response():
	headers = {
		"Content-Type": "text/html"
	}
	return Response("flask handle it automatically", status=200, headers=headers)

if __name__ == "__main__":
	app.run()