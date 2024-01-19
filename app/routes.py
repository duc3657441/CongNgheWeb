from flask import render_template, redirect,url_for, request
from app.connect import connect
from werkzeug.security import generate_password_hash, check_password_hash
from app import app 



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
            query = "SELECT * FROM users WHERE email LIKE %s"
            value = (form_email,)
            cur.execute(query,  value)
            Q = cur.fetchone()
            # return render_template("temp.html",taiKhoan = Q[3], matKhau = Q[4])
           
        except Exception as e:
            return render_template("error.html", message=e)

        # # User exists ?
        if Q is None:
            return render_template("error.html", message="User doesn't exists")
        # Valid password ?
        if not check_password_hash( Q[4], form_password):
            return  render_template("error.html", message = "Invalid password")

        # # Remember which user has logged in
        # # session["user_id"] = Q.userid
        # # session["email"] = Q.email
        # # session["firstname"] = Q.firstname
        # # session["logged_in"] = True
        return redirect(url_for("search"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/search", methods=["GET","POST"])
def search():
    return render_template("search.html")
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     return render_template('login.html')


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     return 'đây là trang register'

# @app.route("/logout")
# def logout():
#     return redirect(url_for("index"))

# @app.route("/search", methods=["GET","POST"])
# def search():
#     return 'đây là trang search'