from app import app, db, api
from flask import render_template, request, Response, json, jsonify, redirect, flash, url_for, session
from app.models import User, Course, Enrollment
from app.forms import LoginForm, RegisterForm
from flask_restplus import Resource
from app.course_list import course_list

#####################################################

@api.route('/api', '/api/')
class GetAndPost(Resource):

    # GET ALL
    def get(self):
        return jsonify(User.objects.all())


    # POST
    def post(self):
       
        data = api.payload

        user = User(user_id=data['user_id'], email=data['email'], 
                    first_name=data['first_name'], last_name=data['last_name'])
        user.set_password(data['password'])
        user.save()
        return jsonify(User.objects(user_id=data['user_id']))

@api.route('/api', '/api/<idx>')
class GetUpdateDelete(Resource):

    # GET One
    def get(self, idx):
        return jsonify(User.objects(user_id=idx))

    # PUT
    def put(self, idx):
        data = api.payload
        User.objects(user_id=idx).update(**data)
        return jsonify(User.objects(user_id=idx))
    
    # DELETE
    def delete(self, idx):
        User.objects(user_id=idx).delete()
        return jsonify("User is deleted")
###################################################


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)


@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term=None):
    if term is None:
        term = 'Spring 2019'
    classes = Course.objects.order_by("-courseID")  # - for descending order
    return render_template(
        "courses.html", courseData=classes, courses=True, term=term
    )


@app.route("/login", methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # form data
        email = form.email.data
        password = form.password.data

        # comapre form email with email in database
        user = User.objects(email=email).first()
        
        if user and user.get_password(password):
        # if request.form.get("email") == "test@uta.com":
            flash("{}, You are successfully logged in".format(user.first_name), "success")
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            return redirect("/index")
        else:
            flash("Sorry, something went wrong", "danger")

    return render_template("login.html", title="Login", form=form, login=True)

@app.route("/logout")
def logout():
    session['user_id'] = False
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if session.get('username'):
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count()
        user_id += 1
        print(user_id)
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        flash("You have registered successfully", "success")
        return redirect(url_for('index'))
    return render_template("register.html", title="Register", form=form, register=True)


@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():

    # If not signed in, goto login page
    if not session.get('username'):
        return redirect(url_for('login'))
    courseID = request.form.get("courseID")
    courseTitle = request.form.get("title")
    user_id = session.get('user_id') 

    if courseID:
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash("Oops, you are already registered in this course {}".format(courseTitle), "danger")
            return redirect(url_for("courses"))
        else:
            Enrollment(user_id=user_id, courseID=courseID).save()
            flash("You are enrolled in {}".format(courseTitle), "success")
    
    classes = course_list()
    return render_template(
        "enrollment.html", enrollment=True, title="Enrollment", classes=classes
    )


# @app.route("/api/")
# @app.route("/api/<idx>")
# def api(idx=None):
#     if not idx:
#         jdata = courseData
#     else:
#         jdata = courseData[int(idx)]

#     # return Response(json.dumps(jdata), mimetype="application/json")


@app.route("/user")
def user():
    # User(user_id=1, first_name="Ayush", last_name="Shah", 
    #      email="ayush.kumar.shah@gmail.com", password="1234").save()
    # User(user_id=2, first_name="Bibash", last_name="Shrestha", 
    #      email="bibash@gmail.com", password="12345").save()
    # User(user_id=3, first_name="Kamlesh", last_name="Kunwar", 
    #      email="kamlesh@gmail.com", password="01234").save()
    users = User.objects.all()
    return render_template("users.html", users=users)
