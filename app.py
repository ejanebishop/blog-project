from flask import Flask

app = Flask(__name__)


@app.route("/home")
def home_page():
    return "Blog Homepage"

@app.route("/login")
def login_page():
    return "Login"




    
if __name__ == "__main__":
    app.run(debug= True)
