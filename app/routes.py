from app import app, db
from flask import render_template, request, Response, json
from app.models import User, Course, Enrollment

courseData = [
    {
        "courseID": "1111",
        "title": "PHP 101",
        "description": "Intro to PHP",
        "credits": 3,
        "term": "Fall, Spring",
    },
    {
        "courseID": "2222",
        "title": "Java 1",
        "description": "Intro to Java Programming",
        "credits": 4,
        "term": "Spring",
    },
    {
        "courseID": "3333",
        "title": "Adv PHP 201",
        "description": "Advanced PHP Programming",
        "credits": 3,
        "term": "Fall",
    },
    {
        "courseID": "4444",
        "title": "Angular 1",
        "description": "Intro to Angular",
        "credits": 3,
        "term": "Fall, Spring",
    },
    {
        "courseID": "5555",
        "title": "Java 2",
        "description": "Advanced Java Programming",
        "credits": 4,
        "term": "Fall",
    },
]


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)


@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term="2019"):
    return render_template(
        "courses.html", courseData=courseData, courses=True, term=term
    )


@app.route("/login")
def login():
    return render_template("login.html", login=True)


@app.route("/register")
def register():
    return render_template("register.html", register=True)


@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    id = request.form.get("courseID")
    title = request.form.get("title")
    term = request.form.get("term")
    return render_template(
        "enrollment.html", register=True, data={"id": id, "term": term, "title": title},
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
