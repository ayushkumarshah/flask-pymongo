from app import app, db
from flask import render_template, request, Response, json, redirect, flash, url_for
from app.models import User, Course, Enrollment
from app.forms import LoginForm, RegisterForm


#         "courseID": "1111",
#         "title": "PHP 101",
#         "description": "Intro to PHP",
#         "credits": 3,
#         "term": "Fall, Spring",
#     },
#     {
#         "courseID": "2222",
#         "title": "Java 1",
#         "description": "Intro to Java Programming",
#         "credits": 4,
#         "term": "Spring",
#     },
#     {
#         "courseID": "3333",
#         "title": "Adv PHP 201",
#         "description": "Advanced PHP Programming",
#         "credits": 3,
#         "term": "Fall",
#     },
#     {
#         "courseID": "4444",
#         "title": "Angular 1",
#         "description": "Intro to Angular",
#         "credits": 3,
#         "term": "Fall, Spring",
#     },
#     {
#         "courseID": "5555",
#         "title": "Java 2",
#         "description": "Advanced Java Programming",
#         "credits": 4,
#         "term": "Fall",
#     },
# # ]


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
            return redirect("/index")
        else:
            flash("Sorry, something went wrong", "danger")

    return render_template("login.html", title="Login", form=form, login=True)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # user_id = User.objects.count()
        user_id = 20
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
    courseID = request.form.get("courseID")
    courseTitle = request.form.get("title")
    user_id = 1

    if courseID:
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash("Oops, you are already registered in this course {}".format(courseTitle), "danger")
            return redirect(url_for("courses"))
        else:
            Enrollment(user_id=user_id, courseID=courseID).save()
            flash("You are enrolled in {}".format(courseTitle), "success")

    classes = None

    term = request.form.get('term')
    return render_template(
        "enrollment.html", enrollment=True, title="Enrollment", classes=classes
    )


@app.route("/api/")
@app.route("/api/<idx>")
def api(idx=None):
    if not idx:
        jdata = courseData
    else:
        jdata = courseData[int(idx)]

    return Response(json.dumps(jdata), mimetype="application/json")


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
