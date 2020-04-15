# for: ROUTES
from flask import Flask, render_template, url_for, redirect, request, flash, abort
# for: DATA
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
# for: FORMS
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

# basically just the app
app = Flask(__name__)

# ========================== DATABASE STUFF ==========================
app.config["SECRET_KEY"] = 'some random key'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)

class Note(db.Model):
    # define parameters for Note class
    # primary_key=True    // unique value
    # nullable=False      // cannot be empty
    # default=""          // default value if none is specified
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(90), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    # how each item will be displayed when called // Note("my note", "4/13/2020")
    def __repr__(self):
        return f"Note('{self.title}', '{self.date_posted}')"

# ============================ FORM STUFF ============================
class NoteForm(FlaskForm):
    author = StringField("Author", validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Submit")

# =========================== ROUTES STUFF ===========================
# function names are descriptive of their purposes
@app.route("/")
@app.route("/home")
def home():
    # ask for (query) all Note items from database
    notes = Note.query.order_by(Note.date_posted.desc()).all()
    # render the home page with the Note items
    return render_template("home.html", title="Home", notes=notes)

@app.route("/note/new", methods=['GET', 'POST'])
def new_note():
    # grab form
    form = NoteForm()
    # if form was submitted
    if form.validate_on_submit():
        # get note data from NoteForm
        note = Note(author=form.author.data, title=form.title.data, content=form.content.data)
        # add note to database
        db.session.add(note)
        db.session.commit()
        # flash message that note was created
        flash("Your note was created!")
        # redirect user to home page using home()
        return redirect(url_for("home"))
    return render_template("create_note.html", title="New Note", form=form)


# ====================================================================

# begins the app on http://127.0.0.1:500/ (port 5000 by default)
if __name__ == "__main__":
    app.run(debug=True)
