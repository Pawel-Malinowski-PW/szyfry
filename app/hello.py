from flask import Flask, render_template, request, make_response
import markdown
<<<<<<< HEAD
import nh3
=======
>>>>>>> f02d5e2c315ee9d24c3877502d2467cffb7ae6ad
from collections import deque

app = Flask(__name__)

notes = []
recent_users = deque(maxlen=3)

<<<<<<< HEAD

ALLOWED_TAGS = {
    'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'blockquote', 'code', 'pre', 'ul', 'ol', 'li', 'a', 'img', 'hr',
    'table', 'thead', 'tbody', 'tr', 'th', 'td'
}

ALLOWED_ATTRIBUTES = {
    'a': {'href', 'title'},
    'img': {'src', 'alt', 'title'},
}

=======
>>>>>>> f02d5e2c315ee9d24c3877502d2467cffb7ae6ad
@app.route("/")
def username():
    return render_template("main.html")

@app.route("/hello", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        username = request.form.get("username", "unknown")
        if not username in recent_users:
            recent_users.append(username)
        resp = make_response(render_template("hello.html", username=username, notes=notes, recent_users=list(recent_users)))
        resp.set_cookie("username", username)
        return resp
    if request.method == 'GET':
        username = request.cookies.get("username", "unknown")
        return render_template("hello.html", username=username, notes=notes, recent_users=list(recent_users))

@app.route("/render", methods=['POST'])
def render():
    md = request.form.get("markdown","")
    rendered = markdown.markdown(md)
<<<<<<< HEAD
    rendered = nh3.clean(rendered, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
=======
>>>>>>> f02d5e2c315ee9d24c3877502d2467cffb7ae6ad
    notes.append(rendered)
    return render_template("markdown.html", rendered=rendered)

@app.route("/render/<rendered_id>")
def render_old(rendered_id):
    if int(rendered_id) > len(notes):
        return "Wrong note id", 404

    rendered = notes[int(rendered_id) - 1]
    return render_template("markdown.html", rendered=rendered)
<<<<<<< HEAD
=======

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
>>>>>>> f02d5e2c315ee9d24c3877502d2467cffb7ae6ad
