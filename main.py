from flask import Flask
app = Flask(__name__)

@app.route("/")
def homePage():
    return "<p>Hello, World!</p>"

app.run(debug=True)