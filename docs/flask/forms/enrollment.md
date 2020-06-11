# Creating aggregation pipeline to create user-course enrollment

## 1. Update enrollment template similar to course template

`enrollment.html`

```html
{% extends 'layout.html' %}

{% block content %}


<div class="row">
        <div class="col-md-12 text-center">

          {% if not classes %}

            <h1>You are not enrolled in any class</h1>

          {% else %}

            <h1>You are enrolled in:</h1>

             
            <table class="table table-hover">
                <thead>
                <tr>
                    <th scope="col">Course ID</th>
                    <th scope="col">Title</th>
                    <th scope="col">Description</th>
                    <th scope="col">Credits</th>
                    <th scope="col">Term</th>
                </tr>
                </thead>
                <tbody>

                <!-- Construct the rest of courses here -->
                
                {% for class in classes %}
                <tr>
                  <td scope='row'>{{class["courseID"]}}</td>
                    <td>{{class["title"]}}</td>
                    <td>{{class["description"]}}</td>
                    <td>{{class["credits"]}}</td>
                    <td>{{class["term"]}}</td>
                </tr>
                {% endfor %}
                </tbody>
            </table>
            {% endif %}

        </div>
</div>
{% endblock %}
```

## 2. Update enrollment route

```python
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
```