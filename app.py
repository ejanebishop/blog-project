from crypt import methods
from flask import Flask, render_template, request, session, redirect
from flask_mysqldb import MySQL
from functools import wraps 
from datetime import datetime
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQl_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ekin.4518'
app.config['MYSQL_DB'] = 'blog'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = 'ajshkjdlfşanfalksşdkalnsf2352'


mysql_db_connection = MySQL(app)

def required_session(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'is_loggedin' in session: 
            return f(*args,**kwargs)
        else:
            return redirect ('/login')
    return wrap


@app.route("/home")
def home_page():
    cursor = mysql_db_connection.connection.cursor()
    select_query = f"SELECT * FROM posts ORDER BY id DESC"
    cursor.execute(select_query)
    posts = cursor.fetchall()
    
    return render_template('home.html', db_posts = posts)

@app.route("/login", methods= ["POST", "GET"])
def login_page():
    #metodu kontrol ediyor
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
       
        cursor = mysql_db_connection.connection.cursor()
     #check user exist
        select_query = f"SELECT * FROM users WHERE email='{email}'"
        cursor.execute(select_query)
        user = cursor.fetchone()
        #user var mı diye kontrol ediyorum
        if user:
            
            #password doğru mu diye kontrol ediyorum.
            if password == user["password"]:
                session["is_loggedin"] = True
                session["email"] = email
                return redirect("/home")

            else: 
               return render_template("loginpage.html", message= "Parolanız yanlıştır. Tekrar deneyiniz.")
                
            

        else:
            return render_template("loginpage.html", message= "Böyle bir kullanıcı bulunamadı.")
        

    return render_template('loginpage.html')
    

@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            return render_template("register.html", message="Şifreler Uyuşmuyor")
        else:
            cursor = mysql_db_connection.connection.cursor()
            #  check user exist
            select_query = f"SELECT * FROM users WHERE email='{email}'"
            cursor.execute(select_query)
            is_user_exist = cursor.fetchall()
            if is_user_exist:
                return render_template("register.html", message="Böyle bir user var zaten!")
            else:
                insert_query = f"INSERT INTO users (email, password) VALUES ('{email}', '{password}');"
                cursor.execute(insert_query)
                mysql_db_connection.connection.commit()
            cursor.close()
            return render_template("register.html", message="Başarıyla kayıt olundu")
    else:
        return render_template('register.html')



        
@app.route("/addpost",methods=["GET", "POST"])
@required_session
def add_post():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("ekin")
        author = session["email"]
        date = datetime.today().strftime('%Y-%m-%d')
        cursor = mysql_db_connection.connection.cursor()
        insert_query = f"INSERT INTO posts (title, created_date, author, content) VALUES ('{title}', '{date}',  '{author}',  '{content}');"
        cursor.execute(insert_query)
        mysql_db_connection.connection.commit()
        cursor.close()
    return render_template('addpost.html')

@app.route("/mypage")
@required_session
def my_page():
        cursor = mysql_db_connection.connection.cursor()
        author = session["email"]
        select_query = f"SELECT * FROM posts WHERE author = '{author}' ORDER BY id DESC"
        cursor.execute(select_query)
        posts = cursor.fetchall()
        return render_template('mypage.html', db_posts = posts)
   

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/post_detail/<post_id>")
def post_detail(post_id):
    cursor = mysql_db_connection.connection.cursor()
    query_string = "SELECT * FROM posts;"
    cursor.execute(query_string)
    
    posts_data = cursor.fetchall()
    cursor.close()
    print(posts_data)

    return render_template('post_detail.html', post_data = posts_data[0])



if __name__ == "__main__":
    app.run(debug= True)
