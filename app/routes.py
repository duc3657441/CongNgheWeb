import requests
from flask import render_template, redirect,url_for, request, session
from app.connect import connect
from werkzeug.security import generate_password_hash, check_password_hash
from app import app 
from functools import wraps

key = "AIzaSyB_W1QyVhMaZV2vFEhW3O02ZB87D20g6gI"
## Helper
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("email") is None:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/register", methods=["GET", "POST"])
def register():

    # if GET, show the registration form
    if request.method == 'GET':
        return render_template('register.html')
    
    # if POST, validate and commit to database
    else:

        #if form values are empty show error

        if not request.form.get("first_name"):
            return render_template("error.html", message="Must provide First Name")
        elif not request.form.get("last_name"):
            return render_template("error.html", message="Must provide Last Name")
        elif  not request.form.get("email"):
            return render_template("error.html", message="Must provide E-mail")
        elif not request.form.get("password1") or not request.form.get("password2"):
            return render_template("error.html", message="Must provide password")
        elif request.form.get("password1") != request.form.get("password2"):
            return render_template("error.html", message="Password does not match")
        else :
            ## assign to variables
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            email = request.form.get("email")
            password = request.form.get("password1")
            # set schema is DatabaseWeb
            
            # try to commit to database, raise error if any
            try:
                conn, cur = connect()
                # cur.execute("SET schema 'DatabaseWeb';")
                insert_script = "INSERT INTO users (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)"
                insert_value = (first_name,last_name,email,generate_password_hash(password))
                cur.execute(insert_script,insert_value)
                conn.commit()
                conn.close()
            except Exception as e:
                return render_template("error.html", message=e)

            #success - redirect to login
            
            return redirect(url_for("login"))
        ## end validation

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form_email = request.form.get("email")
        form_password = request.form.get("password")
        # return render_template("temp.html",taiKhoan = form_email,matKhau = form_password)
        # Ensure username and password was submitted
        if not form_email:
            return render_template("error.html", message="must provide username")
        elif not form_password:
            return render_template("error.html", message="must provide password")
        try:
            conn, cur = connect()
            # cur.execute("SET schema 'DatabaseWeb';")
            # Query database for email and password
            # cur.execute("SELECT * FROM users WHERE email LIKE ':email'", {"email": form_email})
            query = "SELECT UserID, lastName, email, password FROM users WHERE email LIKE %s"
            value = (form_email,)
            cur.execute(query,  value)
            Q = cur.fetchone()
            # return render_template("temp.html",taiKhoan = Q[3], matKhau = Q[4])
            conn.close()
        except Exception as e:
            return render_template("error.html", message=e)

        # # User exists ?
        if Q is None:
            return render_template("error.html", message="User doesn't exists")
        # Valid password ?
        if not check_password_hash( Q[3], form_password):
            return  render_template("error.html", message = "Invalid password")

        # Remember which user has logged in
        session["user_id"] = Q[0]
        session["email"] = Q[2]
        session["lastName"] = Q[1]
        session["logged_in"] = True
        return redirect(url_for("search"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/search", methods=["GET","POST"])
@login_required
def search():
    # return render_template("search.html")
    if request.method == "GET":
        if "lastName" in session:
            name = session["lastName"]
        return render_template("search.html", name = name)
    else:
        query = request.form.get("input-search")
        if query is None:
            return render_template("error.html", message="Search field can not be empty!")
        try:
            conn,cur = connect()
            querySQL = "SELECT isbn, title, author, bookid FROM books WHERE LOWER(isbn) LIKE %s OR LOWER(title) LIKE %s OR LOWER(author) LIKE %s"
            value = "%" + query.lower() + "%"
            valueSQL = (value,value,value)
            # result = db.execute("SELECT * FROM books WHERE LOWER(isbn) LIKE :query OR LOWER(title) LIKE :query OR LOWER(author) LIKE :query", {"query": "%" + query.lower() + "%"}).fetchall()
            cur.execute(querySQL,valueSQL)
            result = cur.fetchall()
            conn.close()
        except Exception as e:
            return render_template("error.html", message=e)
        if not result:
            return render_template("error.html", message="Your query did not match any documents")
        return render_template("list.html", result = result)
        
@app.route("/logout")
@login_required
def logout():
    session.clear()

    return redirect(url_for("index"))

@app.route("/details/<int:bookid>", methods=["GET","POST"])
@login_required
def details(bookid):
    if request.method == "GET":
        try:
            conn, cur = connect()
            querySQL = "SELECT isbn, title, author, year from books WHERE bookid = %s"
            value = (bookid,)
            cur.execute(querySQL,value)
            result = cur.fetchone()
            isbn = result[0]
            conn.close()
        except Exception as e:
            return render_template("error.html", message = e)
        
        try:
            googleapis = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={key}")
        except Exception as e:
            return render_template("error.html", message = e)
        
        # Get comments particular to one book
        try:
            # bookid = '35002'
            conn, cur = connect()
            querySQL = "SELECT u.firstname, u.lastname, u.email, r.rating, r.comment from reviews r JOIN users u ON u.userid=r.user_id WHERE book_id = %s"
            value = (bookid,)
            cur.execute(querySQL,value)
            comment_list = cur.fetchall()
            conn.close()
        except Exception as e:
            return render_template("error.html", message = e)
        
        if comment_list is None:
            return render_template("error.html", message="Invalid book id")
        
        return render_template("details.html", result=result, comment_list=comment_list , bookid=bookid, googleapis=googleapis.json()["items"][0])
    
    # else:
    #     ######## Check if the user commented on this particular book before ###########
    #     conn,cur = connect()
    #     querySQL = "SELECT * from reviews WHERE user_id = %s AND book_id = %s"
    #     value = (session["user_id"], bookid)
    #     cur.execute(querySQL,value)
    #     user_reviewed_before = cur.fetchone()
    #     conn.close()

    #     if user_reviewed_before:
    #         return render_template("error.html", message = "You reviewed this book before!")
        
    #     ######## Proceed to get user comment ###########
    #     user_comment = request.form.get("comments")
    #     user_rating = request.form.get("rating")

    #     if not user_comment:
    #         return render_template("error.html", message="Comment section cannot be empty")

         