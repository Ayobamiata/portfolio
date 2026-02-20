
from flask import Flask, render_template, flash, url_for
from flask_mail import Mail,Message
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy   # <-- SQLAlchemy for ORM
from datetime import datetime             # <-- timestamp each message

from forms import Contact_form

app=Flask(__name__)
app.config['SECRET_KEY']='great'


# app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = 'ayobamiata@yahoo.com'  # your Gmail
# app.config['MAIL_PASSWORD'] = 'ayobamir11..11'     # generated app password
# mail = Mail(app)



# --- Database config (SQLite) ---
# sqlite:///data.db means: use SQLite and store DB in file data.db in project folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# Disable a feature we don't need (saves memory / avoids warnings)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # <-- initialize the ORM with our Flask app


# ------------------ MODELS (tables) ------------------
class ContactMessage(db.Model):
    """
    This class defines the 'contact_messages' table in the SQLite database.
    Each instance is a row in the table.
    """
    __tablename__ = 'contact_messages'            # optional explicit table name
    id = db.Column(db.Integer, primary_key=True)  # unique id for each message
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'ContactMessage {self.id} {self.email}'



@app.route('/')

def home():
    return render_template("index.html")

@app.route('/contact',methods=["GET","POST"])
def contact():
    form=Contact_form()
    if form.validate_on_submit():  #if valid and POSTED
        name=form.Name.data
        email=form.Email.data
        message=form.Message.data

        #--------------to save message to "messages.txt"--------
        with open("messages.txt", "a") as file:
            file.write(f"Name: {name}\nEmail: {email}\nMessage: {message}\n{'-' * 50}\n")


        # ----------to send messages to the mail------------------
        # msg=Message(
        #     subject=f'New message from {name}',
        #     sender=email,
        #     recipients=["ataayobami@yahoo.com"],
        #     body=f'Name:{name}\nEmail:{email}\n\nMessage:\n{message}'
        # )
        #
        # mail.send(msg)

        # --------------to save messages to database---------------------
        new_message = ContactMessage(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()

        flash("Message sent successfully!","success")
        return redirect(url_for("contact"))

    return render_template("contact.html",form=form)


# Admin-ish route: list messages (for quick development viewing)
# Note: in production you should protect this route (login required)
@app.route('/messages')
def messages():
    all_messages = ContactMessage.query.order_by(ContactMessage.timestamp.desc()).all()
    return render_template('messages.html', messages=all_messages)


@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == "__main__":
    with app.app_context():  # ensure Flask app context for SQLAlchemy
        db.create_all()      # create database file and tables if they don't exist
    app.run(debug=True)