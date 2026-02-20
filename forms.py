
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,EmailField,SubmitField
from wtforms.validators import DataRequired


class Contact_form(FlaskForm):
    Name=StringField('NAME',validators=[DataRequired()])
    Email=EmailField('E-MAIL',validators=[DataRequired()])
    Message=TextAreaField("MESSAGE",validators=[DataRequired()])
    Submit=SubmitField('SEND MESSAGE')