from flask import Flask, render_template

app = Flask(__name__)




@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route("/login")
def login_page():
    return render_template('loginpage.html')

@app.route("/register")
def register_page():
    return render_template('register.html')


@app.route("/addpost")
def add_post():
    return render_template('addpost.html')


    
if __name__ == "__main__":
    app.run(debug= True)
